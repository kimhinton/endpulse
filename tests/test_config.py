import pytest

from endpulse.config import load_config, urls_to_configs


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


def test_load_config_invalid(tmp_path):
    config_file = tmp_path / "bad.yaml"
    config_file.write_text("foo: bar")
    with pytest.raises(ValueError, match="must contain an 'endpoints' key"):
        load_config(config_file)
