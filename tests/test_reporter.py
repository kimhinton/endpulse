import json

from endpulse.models import EndpointResult, Status
from endpulse.reporter import _format_bytes, to_json


def test_to_json():
    results = [
        EndpointResult(
            url="https://api.example.com",
            status_code=200,
            response_time_ms=42.5,
            status=Status.UP,
            size_bytes=1024,
        )
    ]
    parsed = json.loads(to_json(results))
    assert len(parsed) == 1
    assert parsed[0]["url"] == "https://api.example.com"
    assert parsed[0]["status"] == "UP"
    assert parsed[0]["response_time_ms"] == 42.5


def test_format_bytes():
    assert _format_bytes(500) == "500B"
    assert _format_bytes(1024) == "1.0KB"
    assert _format_bytes(1536) == "1.5KB"
    assert _format_bytes(1048576) == "1.0MB"
