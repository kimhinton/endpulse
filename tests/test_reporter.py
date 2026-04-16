import json

from endpulse.models import EndpointResult, SSLInfo, Status
from endpulse.reporter import _format_bytes, has_failures, to_csv, to_json, to_markdown


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


def test_to_json_with_ssl():
    results = [
        EndpointResult(
            url="https://api.example.com",
            status_code=200,
            response_time_ms=42.5,
            status=Status.UP,
            size_bytes=1024,
            ssl_info=SSLInfo(
                issuer="CN=Test CA",
                expires="Dec 31 2025 GMT",
                days_remaining=90,
            ),
        )
    ]
    parsed = json.loads(to_json(results))
    assert parsed[0]["ssl"]["days_remaining"] == 90
    assert parsed[0]["ssl"]["issuer"] == "CN=Test CA"


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


def test_to_markdown():
    results = [
        EndpointResult(
            url="https://api.example.com",
            status_code=200,
            response_time_ms=42.5,
            status=Status.UP,
            size_bytes=1024,
        ),
        EndpointResult(
            url="https://api2.example.com",
            status_code=500,
            response_time_ms=150.0,
            status=Status.ERROR,
            size_bytes=256,
        ),
    ]
    md = to_markdown(results)
    assert "## Endpoint Health Report" in md
    assert "`https://api.example.com`" in md
    assert "**UP**" in md
    assert "**ERROR**" in md
    assert "**1/2** endpoints up" in md
    assert "**1 failed**" in md


def test_to_markdown_with_ssl():
    results = [
        EndpointResult(
            url="https://api.example.com",
            status_code=200,
            response_time_ms=42.5,
            status=Status.UP,
            size_bytes=1024,
            ssl_info=SSLInfo(days_remaining=45),
        ),
    ]
    md = to_markdown(results, show_ssl=True)
    assert "SSL Expiry" in md
    assert "45d" in md


def test_to_csv():
    results = [
        EndpointResult(
            url="https://api.example.com",
            status_code=200,
            response_time_ms=42.5,
            status=Status.UP,
            size_bytes=1024,
        ),
    ]
    output = to_csv(results)
    lines = output.strip().split("\n")
    assert len(lines) == 2
    assert "url,status,status_code" in lines[0]
    assert "https://api.example.com,UP,200" in lines[1]


def test_to_csv_with_ssl():
    results = [
        EndpointResult(
            url="https://api.example.com",
            status_code=200,
            response_time_ms=42.5,
            status=Status.UP,
            size_bytes=1024,
            ssl_info=SSLInfo(days_remaining=90, expires="Dec 31 2025 GMT"),
        ),
    ]
    output = to_csv(results, show_ssl=True)
    assert "ssl_days_remaining" in output
    assert "90" in output
