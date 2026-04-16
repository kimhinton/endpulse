from endpulse.models import Assertion, EndpointConfig, EndpointResult, SSLInfo, Status


def test_endpoint_result_defaults():
    r = EndpointResult(url="https://example.com")
    assert r.status == Status.DOWN
    assert r.status_code is None
    assert r.response_time_ms == 0.0
    assert r.error is None
    assert r.size_bytes == 0
    assert r.body is None
    assert r.failed_assertions == []
    assert r.ssl_info is None


def test_endpoint_config_defaults():
    c = EndpointConfig(url="https://example.com")
    assert c.method == "GET"
    assert c.expected_status == 200
    assert c.timeout == 10.0
    assert c.threshold_ms == 1000.0
    assert c.assertions == []


def test_status_values():
    assert Status.UP.value == "UP"
    assert Status.DOWN.value == "DOWN"
    assert Status.SLOW.value == "SLOW"
    assert Status.ERROR.value == "ERROR"


def test_assertion_body_contains():
    result = EndpointResult(url="https://example.com", body='{"status": "ok"}')
    a = Assertion(type="body_contains", value="ok")
    assert a.check(result) is True

    a2 = Assertion(type="body_contains", value="error")
    assert a2.check(result) is False


def test_assertion_body_regex():
    result = EndpointResult(url="https://example.com", body='{"version": "1.2.3"}')
    a = Assertion(type="body_regex", value=r"\d+\.\d+\.\d+")
    assert a.check(result) is True

    a2 = Assertion(type="body_regex", value=r"^error$")
    assert a2.check(result) is False


def test_assertion_header_contains():
    result = EndpointResult(
        url="https://example.com",
        headers={"content-type": "application/json; charset=utf-8"},
    )
    a = Assertion(type="header_contains", value="content-type:json")
    assert a.check(result) is True


def test_assertion_status():
    result = EndpointResult(url="https://example.com", status_code=201)
    a = Assertion(type="status", value="201")
    assert a.check(result) is True

    a2 = Assertion(type="status", value="200")
    assert a2.check(result) is False


def test_assertion_describe():
    a = Assertion(type="body_contains", value="ok")
    assert a.describe() == "body_contains=ok"


def test_ssl_info_defaults():
    s = SSLInfo()
    assert s.issuer == ""
    assert s.subject == ""
    assert s.expires == ""
    assert s.days_remaining == 0
    assert s.error is None


def test_ssl_info_with_data():
    s = SSLInfo(
        issuer="CN=Let's Encrypt",
        subject="CN=example.com",
        expires="Dec 31 23:59:59 2025 GMT",
        days_remaining=90,
    )
    assert s.days_remaining == 90
    assert "Let's Encrypt" in s.issuer


def test_endpoint_result_with_ssl():
    ssl = SSLInfo(days_remaining=45, expires="Jun 30 2025 GMT")
    r = EndpointResult(
        url="https://example.com",
        status=Status.UP,
        ssl_info=ssl,
    )
    assert r.ssl_info is not None
    assert r.ssl_info.days_remaining == 45
