from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    UP = "UP"
    DOWN = "DOWN"
    SLOW = "SLOW"
    ERROR = "ERROR"


@dataclass
class EndpointResult:
    url: str
    status_code: int | None = None
    response_time_ms: float = 0.0
    status: Status = Status.DOWN
    error: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    size_bytes: int = 0


@dataclass
class EndpointConfig:
    url: str
    method: str = "GET"
    expected_status: int = 200
    timeout: float = 10.0
    headers: dict[str, str] = field(default_factory=dict)
    threshold_ms: float = 1000.0
