import httpx
import pytest
import respx

from endpulse.models import EndpointResult, Status
from endpulse.notifier import (
    detect_webhook_type,
    format_discord_payload,
    format_generic_payload,
    format_slack_payload,
    notify_all,
    send_notification,
)


def test_detect_webhook_type():
    assert detect_webhook_type("https://hooks.slack.com/services/T00/B00/xxx") == "slack"
    assert detect_webhook_type("https://discord.com/api/webhooks/123/abc") == "discord"
    assert detect_webhook_type("https://example.com/webhook") == "generic"


def test_format_slack_payload_with_failures():
    results = [
        EndpointResult(url="https://a.com", status=Status.DOWN, error="Timeout"),
        EndpointResult(url="https://b.com", status=Status.UP),
    ]
    payload = format_slack_payload(results)
    assert payload is not None
    assert "1 endpoint(s) failing" in payload["text"]
    assert "https://a.com" in payload["text"]


def test_format_slack_payload_no_failures():
    results = [
        EndpointResult(url="https://a.com", status=Status.UP),
    ]
    payload = format_slack_payload(results)
    assert payload is None


def test_format_discord_payload_with_failures():
    results = [
        EndpointResult(url="https://a.com", status=Status.ERROR),
    ]
    payload = format_discord_payload(results)
    assert payload is not None
    assert "1 endpoint(s) failing" in payload["content"]


def test_format_discord_payload_no_failures():
    results = [
        EndpointResult(url="https://a.com", status=Status.UP),
    ]
    payload = format_discord_payload(results)
    assert payload is None


def test_format_generic_payload():
    results = [
        EndpointResult(
            url="https://a.com", status=Status.UP, status_code=200, response_time_ms=50.0,
        ),
        EndpointResult(url="https://b.com", status=Status.DOWN, error="Timeout"),
    ]
    payload = format_generic_payload(results)
    assert payload["status"] == "failure"
    assert payload["total"] == 2
    assert payload["failed"] == 1
    assert len(payload["results"]) == 2


def test_format_generic_payload_all_ok():
    results = [
        EndpointResult(url="https://a.com", status=Status.UP),
    ]
    payload = format_generic_payload(results)
    assert payload["status"] == "ok"
    assert payload["failed"] == 0


@respx.mock
@pytest.mark.asyncio
async def test_send_notification_success():
    respx.post("https://example.com/webhook").mock(
        return_value=httpx.Response(200)
    )
    results = [
        EndpointResult(url="https://a.com", status=Status.DOWN, error="Timeout"),
    ]
    ok = await send_notification("https://example.com/webhook", results)
    assert ok is True


@respx.mock
@pytest.mark.asyncio
async def test_send_notification_no_failures():
    results = [
        EndpointResult(url="https://a.com", status=Status.UP),
    ]
    ok = await send_notification("https://example.com/webhook", results)
    assert ok is True


@respx.mock
@pytest.mark.asyncio
async def test_notify_all():
    respx.post("https://example.com/hook1").mock(
        return_value=httpx.Response(200)
    )
    respx.post("https://example.com/hook2").mock(
        return_value=httpx.Response(200)
    )
    results = [
        EndpointResult(url="https://a.com", status=Status.DOWN, error="Timeout"),
    ]
    statuses = await notify_all(
        ["https://example.com/hook1", "https://example.com/hook2"],
        results,
    )
    assert all(statuses)
