from endpulse.ssl_checker import check_ssl


def test_check_ssl_not_https():
    info = check_ssl("http://example.com")
    assert info.error == "Not HTTPS"


def test_check_ssl_invalid_host():
    info = check_ssl("https://this-host-does-not-exist-12345.example.com", timeout=3.0)
    assert info.error is not None
