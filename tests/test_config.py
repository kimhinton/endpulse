import pytest

from endpulse.config import load_config, parse_cli_assertions, urls_to_configs


def test_urls_to_configs():
    configs = urls_to_configs(["https://a.com", "https://b.com"], timeout=5.0)
    assert len(configs) == 2
    assert configs[0].url == "https://a.com"
    assert configs[0].timeout == 5.0
    assert configs[1].url == "https://b.com"


def test_load_config(tmp_path):
    config_file = tmp_path / "endpoints.yaml"
    config_file.write_text(
        """
defaults:
  timeout: 5
  threshold_ms: 500

endpoints:
  - https://api.example.com/health
  - url: https://api.example.com/v2/status
    method: POST
    expected_status: 201
"""
    )
    configs = load_config(config_file)
    assert len(configs) == 2
    assert configs[0].url == "https://api.example.com/health"
    assert configs[0].timeout == 5
    assert configs[0].threshold_ms == 500
    assert configs[1].method == "POST"
    assert configs[1].expected_status == 201


def test_load_config_with_assertions(tmp_path):
    config_file = tmp_path / "endpoints.yaml"
    config_file.write_text(
        """
endpoints:
  - url: https://api.example.com/health
    assert:
      - "body_contains:ok"
      - "header_contains:content-type:json"
"""
    )
    configs = load_config(config_file)
    assert len(configs) == 1
    assert len(configs[0].assertions) == 2
    assert configs[0].assertions[0].type == "body_contains"
    assert configs[0].assertions[0].value == "ok"
    assert configs[0].assertions[1].type == "header_contains"
    assert configs[0].assertions[1].value == "content-type:json"


def test_load_config_invalid(tmp_path):
    config_file = tmp_path / "bad.yaml"
    config_file.write_text("foo: bar")
    with pytest.raises(ValueError, match="must contain an 'endpoints' key"):
        load_config(config_file)


def test_parse_cli_assertions():
    raw = ("body_contains:ok", "status:200")
    assertions = parse_cli_assertions(raw)
    assert len(assertions) == 2
    assert assertions[0].type == "body_contains"
    assert assertions[0].value == "ok"
    assert assertions[1].type == "status"
    assert assertions[1].value == "200"
