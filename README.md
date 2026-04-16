# endpulse

[![CI](https://github.com/kimhinton/endpulse/actions/workflows/ci.yml/badge.svg)](https://github.com/kimhinton/endpulse/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Lightweight CLI tool for API endpoint health checking and response time monitoring.

![endpulse demo](https://raw.githubusercontent.com/kimhinton/endpulse/main/docs/demo.png)

## Features

- **Async health checks** — concurrent requests with configurable concurrency limit
- **Response time tracking** — measures latency per endpoint with slow-response detection
- **YAML config** — define endpoints, thresholds, and headers in a config file
- **Rich terminal output** — color-coded status table with summary stats
- **JSON output** — pipe results to monitoring systems or dashboards
- **Multi-round runs** — repeat checks to detect intermittent failures
- **Cross-platform** — works on Linux, macOS, and Windows

## Installation

```bash
pip install endpulse
```

Or install from source:

```bash
git clone https://github.com/kimhinton/endpulse.git
cd endpulse
pip install -e .
```

## Quick Start

Check a single endpoint:

```bash
endpulse https://api.example.com/health
```

Check multiple endpoints:

```bash
endpulse https://api1.example.com https://api2.example.com https://api3.example.com
```

Use a config file:

```bash
endpulse -c endpoints.yaml
```

## Usage

```
Usage: endpulse [OPTIONS] [URLS]...

Options:
  -c, --config PATH      YAML config file
  -n, --repeat INTEGER   Number of rounds to run  [default: 1]
  -t, --timeout FLOAT    Request timeout in seconds  [default: 10.0]
  --threshold FLOAT      Slow response threshold in ms  [default: 1000.0]
  --method TEXT           HTTP method  [default: GET]
  --concurrency INTEGER  Max concurrent requests  [default: 10]
  --json                 Output as JSON
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

## Config File

Create an `endpoints.yaml` file:

```yaml
defaults:
  timeout: 10
  threshold_ms: 800
  method: GET

endpoints:
  - https://api.example.com/health
  - https://api.example.com/v2/status

  - url: https://api.example.com/webhook
    method: POST
    expected_status: 201
    timeout: 5
```

Then run:

```bash
endpulse -c endpoints.yaml
```

## Output Examples

### Table (default)

```
┌──────────────────────────────────┬──────────┬────────┬──────────────┬────────────┬───────┐
│ URL                              │  Status  │  Code  │    Time (ms) │       Size │ Error │
├──────────────────────────────────┼──────────┼────────┼──────────────┼────────────┼───────┤
│ https://api.example.com/health   │    UP    │  200   │         42.3 │     1.2KB  │       │
│ https://api.example.com/v2       │   SLOW   │  200   │       1523.7 │     4.8KB  │       │
│ https://api.broken.com/health    │   DOWN   │   -    │      10001.2 │         -  │ Timeout│
└──────────────────────────────────┴──────────┴────────┴──────────────┴────────────┴───────┘

2/3 endpoints up  |  avg response: 3855.7ms
```

### JSON

```bash
endpulse https://api.example.com/health --json
```

```json
[
  {
    "url": "https://api.example.com/health",
    "status": "UP",
    "status_code": 200,
    "response_time_ms": 42.3,
    "size_bytes": 1234,
    "error": null
  }
]
```

## Development

```bash
git clone https://github.com/kimhinton/endpulse.git
cd endpulse
pip install -e ".[dev]"

# Run tests
pytest -v

# Lint
ruff check endpulse/ tests/

# Type check
mypy endpulse/
```

## License

[MIT](LICENSE)
