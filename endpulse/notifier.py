from __future__ import annotations

import json

import httpx

from endpulse.models import EndpointResult, Status


def detect_webhook_type(url: str) -> str:
    """Auto-detect webhook type from URL."""
    if "hooks.slack.com" in url:
        return "slack"
    if "discord.com/api/webhooks" in url:
        return "discord"
    return "generic"


def format_slack_payload(results: list[EndpointResult]) -> dict[str, object] | None:
    """Format results as a Slack incoming webhook payload. Returns None if no failures."""
    failed = [r for r in results if r.status in (Status.DOWN, Status.ERROR)]
    if not failed:
        return None

    lines = [f"*{len(failed)} endpoint(s) failing*\n"]
    for r in failed:
        error_info = r.error or ", ".join(r.failed_assertions) or ""
        lines.append(f"  `{r.url}` -- {r.status.value} {error_info}")

    return {"text": "\n".join(lines)}


def format_discord_payload(results: list[EndpointResult]) -> dict[str, object] | None:
    """Format results as a Discord webhook payload. Returns None if no failures."""
    failed = [r for r in results if r.status in (Status.DOWN, Status.ERROR)]
    if not failed:
        return None

    lines = [f"**{len(failed)} endpoint(s) failing**\n"]
    for r in failed:
        error_info = r.error or ", ".join(r.failed_assertions) or ""
        lines.append(f"- `{r.url}` -- {r.status.value} {error_info}")

    return {"content": "\n".join(lines)}


def format_generic_payload(
    results: list[EndpointResult],
) -> dict[str, object]:
    """Format results as a generic JSON webhook payload. Always returns payload."""
    return {
        "status": (
            "failure"
            if any(r.status in (Status.DOWN, Status.ERROR) for r in results)
            else "ok"
        ),
        "total": len(results),
        "failed": sum(
            1 for r in results if r.status in (Status.DOWN, Status.ERROR)
        ),
        "results": [
            {
                "url": r.url,
                "status": r.status.value,
                "status_code": r.status_code,
                "response_time_ms": r.response_time_ms,
                "error": r.error,
            }
            for r in results
        ],
    }


async def send_notification(
    webhook_url: str,
    results: list[EndpointResult],
    *,
    only_on_failure: bool = True,
) -> bool:
    """Send notification to a webhook URL. Returns True on success."""
    webhook_type = detect_webhook_type(webhook_url)

    payload: dict[str, object] | None
    if webhook_type == "slack":
        payload = format_slack_payload(results)
    elif webhook_type == "discord":
        payload = format_discord_payload(results)
    else:
        payload = format_generic_payload(results)

    if payload is None:
        return True

    if only_on_failure and not any(
        r.status in (Status.DOWN, Status.ERROR) for r in results
    ):
        return True

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url,
                content=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10.0,
            )
            return response.status_code < 400
    except httpx.RequestError:
        return False


async def notify_all(
    webhook_urls: list[str],
    results: list[EndpointResult],
) -> list[bool]:
    """Send notifications to all configured webhooks."""
    statuses = []
    for url in webhook_urls:
        ok = await send_notification(url, results)
        statuses.append(ok)
    return statuses
