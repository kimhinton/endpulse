from __future__ import annotations

from pathlib import Path

import yaml

from endpulse.models import EndpointConfig


def load_config(path: Path) -> list[EndpointConfig]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict) or "endpoints" not in data:
        raise ValueError(f"Invalid config: {path} must contain an 'endpoints' key")

    defaults = data.get("defaults", {})
    configs = []

    for ep in data["endpoints"]:
        if isinstance(ep, str):
            ep = {"url": ep}

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
            )
        )

    return configs


def urls_to_configs(
    urls: list[str],
    method: str = "GET",
    timeout: float = 10.0,
    threshold_ms: float = 1000.0,
) -> list[EndpointConfig]:
    return [
        EndpointConfig(
            url=url, method=method, timeout=timeout, threshold_ms=threshold_ms
        )
        for url in urls
    ]
