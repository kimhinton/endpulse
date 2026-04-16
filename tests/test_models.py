from endpulse.models import EndpointConfig, EndpointResult, Status


def test_endpoint_result_defaults():
    r = EndpointResult(url="https://example.com")
    assert r.status == Status.DOWN
    assert r.status_code is None
    assert r.response_time_ms == 0.0
    assert r.error is None
    assert r.size_bytes == 0


def test_endpoint_config_defaults():
    c = EndpointConfig(url="https://example.com")
    assert c.method == "GET"
    assert c.expected_status == 200
    assert c.timeout == 10.0
    assert c.threshold_ms == 1000.0


def test_status_values():
    assert Status.UP.value == "UP"
    assert Status.DOWN.value == "DOWN"
    assert Status.SLOW.value == "SLOW"
    assert Status.ERROR.value == "ERROR"
