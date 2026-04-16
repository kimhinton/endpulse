# endpulse

[![CI](https://github.com/kimhinton/endpulse/actions/workflows/ci.yml/badge.svg)](https://github.com/kimhinton/endpulse/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Lightweight CLI for API endpoint health checking with assertions, watch mode, and CI-friendly exit codes.

```bash
pip install endpulse
```

```bash
# Check a single endpoint
endpulse https://api.example.com/health

# Check multiple endpoints with a slow threshold
endpulse https://api1.com https://api2.com --threshold 500

# Assert response body and fail CI if unhealthy
endpulse https://api.example.com/health --fail -a "body_contains:ok"

# Watch mode — re-check every 5 seconds
endpulse -c endpoints.yaml -w 5
```

## Why endpulse?

Most HTTP tools are either **one-shot clients** (httpie, curl) or **heavy load testers** (k6, Locust).

endpulse fills the gap: **multi-endpoint health checks with assertions, in a single command.**

- Check 50 endpoints concurrently in seconds
- Assert response body, headers, and status codes
- `--fail` exits with code 1 on failure — plug directly into CI/CD
- `--watch` mode for continuous monitoring in your terminal
- YAML config for defining all your endpoints in one file

## Features

- **Async concurrent checks** — semaphore-bounded, configurable concurrency
- **Response assertions** — body contains, body regex, header match, status code
- **Watch mode** — continuous monitoring with live-updating terminal table
- **CI/CD integration** — `--fail` flag returns exit code 1 on any failure
- **YAML config** — define endpoints, thresholds, headers, and assertions
- **Rich terminal output** — color-coded status with timing and size
- **JSON output** — `--json` for piping to monitoring systems
- **Cross-platform** — Linux, macOS, Windows

## Usage

```
endpulse [OPTIONS] [URLS]...

Options:
  -c, --config PATH       YAML config file
  -n, --repeat INTEGER    Number of rounds to run  [default: 1]
  -t, --timeout FLOAT     Request timeout in seconds  [default: 10.0]
  --threshold FLOAT       Slow response threshold in ms  [default: 1000.0]
  --method TEXT            HTTP method  [default: GET]
  --concurrency INTEGER   Max concurrent requests  [default: 10]
  --json                  Output as JSON
  --fail                  Exit code 1 if any endpoint fails
  -a, --assert TEXT       Assertion (repeatable)
  -w, --watch FLOAT       Watch mode interval in seconds
  --version               Show version and exit
  --help                  Show this message and exit
```

## Assertions

Assert response content directly from the CLI:

```bash
# Body contains text
endpulse https://api.example.com -a "body_contains:ok"

# Body matches regex
endpulse https://api.example.com -a "body_regex:version.*\d+\.\d+"

# Header contains value
endpulse https://api.example.com -a "header_contains:content-type:json"

# Status code check
endpulse https://api.example.com -a "status:200"

# Multiple assertions
endpulse https://api.example.com -a "body_contains:ok" -a "status:200" --fail
```

## Config File

```yaml
# endpoints.yaml
defaults:
  timeout: 10
  threshold_ms: 800

endpoints:
  - https://api.example.com/health

  - url: https://api.example.com/v2/status
    method: POST
    expected_status: 201
    assert:
      - "body_contains:ok"
      - "header_contains:content-type:json"

  - url: https://api.example.com/slow
    threshold_ms: 3000
    timeout: 5
```

```bash
endpulse -c endpoints.yaml --fail
```

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Health check
  run: |
    pip install endpulse
    endpulse -c endpoints.yaml --fail
```

The `--fail` flag makes endpulse return exit code 1 when any endpoint is DOWN or fails an assertion — your pipeline stops on unhealthy services.

## Watch Mode

Monitor endpoints continuously:

```bash
# Re-check every 5 seconds
endpulse https://api1.com https://api2.com -w 5

# Watch with failure alerting
endpulse -c endpoints.yaml -w 10 --fail
```

The terminal table updates in-place with each round. Press `Ctrl+C` to stop.

## Development

```bash
git clone https://github.com/kimhinton/endpulse.git
cd endpulse
pip install -e ".[dev]"
pytest -v
ruff check endpulse/ tests/
mypy endpulse/
```

## License

[MIT](LICENSE)
