from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    UP = "UP"
    DOWN = "DOWN"
    SLOW = "SLOW"
    ERROR = "ERROR"


@dataclass
class SSLInfo:
    issuer: str = ""
    subject: str = ""
    expires: str = ""
    days_remaining: int = 0
    error: str | None = None


@dataclass
class Assertion:
    type: str  # "status", "body_contains", "body_regex", "header_contains"
    value: str

    def check(self, result: EndpointResult) -> bool:
        if self.type == "status":
            return str(result.status_code) == self.value
        if self.type == "body_contains":
            return self.value in (result.body or "")
        if self.type == "body_regex":
            return bool(re.search(self.value, result.body or ""))
        if self.type == "header_contains":
            key, _, val = self.value.partition(":")
            header_val = result.headers.get(key.strip().lower(), "")
            return val.strip() in header_val
        return False

    def describe(self) -> str:
        return f"{self.type}={self.value}"


@dataclass
class EndpointResult:
    url: str
    status_code: int | None = None
    response_time_ms: float = 0.0
    status: Status = Status.DOWN
    error: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    size_bytes: int = 0
    body: str | None = None
    failed_assertions: list[str] = field(default_factory=list)
    ssl_info: SSLInfo | None = None


@dataclass
class EndpointConfig:
    url: str
    method: str = "GET"
    expected_status: int = 200
    timeout: float = 10.0
    headers: dict[str, str] = field(default_factory=dict)
    threshold_ms: float = 1000.0
    assertions: list[Assertion] = field(default_factory=list)
