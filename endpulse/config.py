from __future__ import annotations

from pathlib import Path

import yaml

from endpulse.models import Assertion, EndpointConfig

INIT_TEMPLATE = """\
# endpulse configuration
# Usage: endpulse -c endpoints.yaml
# Docs:  https://github.com/kimhinton/endpulse

defaults:
  timeout: 10
  threshold_ms: 1000
  method: GET

# Webhook notifications (optional)
# Sends alert when any endpoint fails
# Supports Slack, Discord, or any generic webhook
#
# notify:
#   - https://hooks.slack.com/services/YOUR/WEBHOOK/URL
#   - https://discord.com/api/webhooks/YOUR/WEBHOOK

endpoints:
  # Simple URL format
  - https://your-api.com/health

  # Detailed format with assertions
  - url: https://your-api.com/v2/status
    method: GET
    timeout: 5
    threshold_ms: 500
    assert:
      - "body_contains:ok"
      - "status:200"
      - "header_contains:content-type:json"

  # POST endpoint with custom expected status
  - url: https://your-api.com/webhook
    method: POST
    expected_status: 201
    timeout: 5

  # Endpoint with higher threshold for slow services
  - url: https://your-api.com/reports
    threshold_ms: 5000
    timeout: 15
"""


def generate_init_config(path: Path) -> Path:
    """Generate a sample endpoints.yaml config file."""
    output = path / "endpoints.yaml"
    output.write_text(INIT_TEMPLATE, encoding="utf-8")
    return output


def load_config(path: Path) -> tuple[list[EndpointConfig], list[str]]:
    """Load config from YAML. Returns (endpoint_configs, notify_urls)."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict) or "endpoints" not in data:
        raise ValueError(f"Invalid config: {path} must contain an 'endpoints' key")

    defaults = data.get("defaults", {})
    notify_urls: list[str] = data.get("notify", [])
    if isinstance(notify_urls, str):
        notify_urls = [notify_urls]

    configs = []

    for ep in data["endpoints"]:
        if isinstance(ep, str):
            ep = {"url": ep}

        assertions = _parse_assertions(ep.get("assert", []))

        configs.append(
            EndpointConfig(
                url=ep["url"],
                method=ep.get("method", defaults.get("method", "GET")),
                expected_status=ep.get(
                    "expected_status", defaults.get("expected_status", 200)
                ),
                timeout=ep.get("timeout", defaults.get("timeout", 10.0)),
                headers={**defaults.get("headers", {}), **ep.get("headers", {})},
                threshold_ms=ep.get(
                    "threshold_ms", defaults.get("threshold_ms", 1000.0)
                ),
                assertions=assertions,
            )
        )

    return configs, notify_urls


def _parse_assertions(raw: list[str] | str) -> list[Assertion]:
    if isinstance(raw, str):
        raw = [raw]
    assertions = []
    for item in raw:
        if ":" in item:
            atype, _, avalue = item.partition(":")
            assertions.append(Assertion(type=atype.strip(), value=avalue.strip()))
    return assertions


def urls_to_configs(
    urls: list[str],
    method: str = "GET",
    timeout: float = 10.0,
    threshold_ms: float = 1000.0,
    assertions: list[Assertion] | None = None,
) -> list[EndpointConfig]:
    return [
        EndpointConfig(
            url=url,
            method=method,
            timeout=timeout,
            threshold_ms=threshold_ms,
            assertions=assertions or [],
        )
        for url in urls
    ]


def parse_cli_assertions(raw_assertions: tuple[str, ...]) -> list[Assertion]:
    assertions = []
    for item in raw_assertions:
        if ":" in item:
            atype, _, avalue = item.partition(":")
            assertions.append(Assertion(type=atype.strip(), value=avalue.strip()))
    return assertions
