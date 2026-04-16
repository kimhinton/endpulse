import json

from endpulse.models import EndpointResult, Status
from endpulse.reporter import _format_bytes, has_failures, to_json


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
    assert parsed[0]["failed_assertions"] is None


def test_to_json_with_failed_assertions():
    results = [
        EndpointResult(
            url="https://api.example.com",
            status_code=200,
            response_time_ms=42.5,
            status=Status.ERROR,
            size_bytes=1024,
            failed_assertions=["body_contains=healthy"],
        )
    ]
    parsed = json.loads(to_json(results))
    assert parsed[0]["failed_assertions"] == ["body_contains=healthy"]


def test_format_bytes():
    assert _format_bytes(500) == "500B"
    assert _format_bytes(1024) == "1.0KB"
    assert _format_bytes(1536) == "1.5KB"
    assert _format_bytes(1048576) == "1.0MB"


def test_has_failures():
    results_ok = [
        EndpointResult(url="https://a.com", status=Status.UP),
        EndpointResult(url="https://b.com", status=Status.SLOW),
    ]
    assert has_failures(results_ok) is False

    results_bad = [
        EndpointResult(url="https://a.com", status=Status.UP),
        EndpointResult(url="https://b.com", status=Status.DOWN),
    ]
    assert has_failures(results_bad) is True
