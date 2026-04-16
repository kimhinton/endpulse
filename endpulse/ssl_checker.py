from __future__ import annotations

import socket
import ssl
import time
from typing import Any
from urllib.parse import urlparse

from endpulse.models import SSLInfo


def _extract_cert_field(raw: Any) -> str:
    """Extract a human-readable string from a certificate issuer/subject field."""
    parts: list[str] = []
    if isinstance(raw, tuple):
        for entry in raw:
            if isinstance(entry, tuple):
                for pair in entry:
                    if isinstance(pair, tuple) and len(pair) == 2:
                        parts.append(f"{pair[0]}={pair[1]}")
    return ", ".join(parts)


def check_ssl(url: str, timeout: float = 10.0) -> SSLInfo:
    """Check SSL certificate for a given URL and return expiry info."""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return SSLInfo(error="Not HTTPS")

    hostname = parsed.hostname or ""
    port = parsed.port or 443

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        if not cert:
            return SSLInfo(error="No certificate")

        not_after_raw = cert.get("notAfter", "")
        not_after_str = str(not_after_raw)
        not_after_ts = ssl.cert_time_to_seconds(not_after_str)
        days_remaining = int((not_after_ts - time.time()) / 86400)

        issuer = _extract_cert_field(cert.get("issuer", ()))
        subject = _extract_cert_field(cert.get("subject", ()))

        return SSLInfo(
            issuer=issuer,
            subject=subject,
            expires=not_after_str,
            days_remaining=days_remaining,
        )
    except Exception as e:
        return SSLInfo(error=str(e))
