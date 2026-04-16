# endpulse

[![CI](https://github.com/kimhinton/endpulse/actions/workflows/ci.yml/badge.svg)](https://github.com/kimhinton/endpulse/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/endpulse.svg)](https://pypi.org/project/endpulse/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Multi-endpoint API health checks with assertions, SSL monitoring, and CI exit codes — in a single command.**

```bash
pip install endpulse
```

```
$ endpulse https://api.example.com/health https://api.example.com/v2/status --ssl

┌──────────────────────────────────────────────────────────────────────────────────┐
│                              Endpoint Health Report                              │
├──────────────────────────────────┬────────┬──────┬──────────┬───────┬────────────┤
│ URL                              │ Status │ Code │ Time(ms) │ Size  │ SSL Expiry │
├──────────────────────────────────┼────────┼──────┼──────────┼───────┼────────────┤
│ https://api.example.com/health   │   UP   │ 200  │    42.5  │ 1.2KB │   89d      │
│ https://api.example.com/v2/status│   UP   │ 200  │   118.3  │ 2.4KB │   89d      │
└──────────────────────────────────┴────────┴──────┴──────────┴───────┴────────────┘

2/2 endpoints up  |  avg response: 80.4ms
```

## Why endpulse?

Most HTTP tools are either **one-shot clients** (httpie, curl) or **heavy infrastructure** (k6, Uptime Kuma, Gatus).

endpulse fills the gap:

| Feature | curl/httpie | k6/Artillery | Uptime Kuma | endpulse |
|---------|:-----------:|:------------:|:-----------:|:--------:|
| Multi-endpoint in one command | - | - | - | **yes** |
| Response assertions (body, headers) | - | script | UI | **CLI flags** |
| CI/CD exit codes | manual | yes | - | **yes** |
| Watch mode (live terminal) | - | - | web UI | **yes** |
| SSL certificate monitoring | - | - | yes | **yes** |
| Webhook alerts (Slack/Discord) | - | plugin | yes | **yes** |
| Zero infrastructure | yes | yes | no | **yes** |
| YAML config | - | JS/YAML | UI | **yes** |

## Features

- **Async concurrent checks** — semaphore-bounded, configurable concurrency
- **Response assertions** — body contains, body regex, header match, status code
- **SSL certificate monitoring** — check expiry dates with `--ssl`
- **Watch mode** — continuous monitoring with live-updating terminal table
- **Webhook notifications** — Slack, Discord, or generic webhook on failures
- **CI/CD integration** — `--fail` flag returns exit code 1 on any failure
- **Multiple output formats** — table, JSON, Markdown, CSV
- **YAML config** — define endpoints, thresholds, headers, and assertions
- **Rich terminal output** — color-coded status with timing and size
- **Cross-platform** — Linux, macOS, Windows

## Quick Start

```bash
# Check a single endpoint
endpulse https://api.example.com/health

# Check multiple endpoints with a slow threshold
endpulse https://api1.com https://api2.com --threshold 500

# Assert response body and fail CI if unhealthy
endpulse https://api.example.com/health --fail -a "body_contains:ok"

# Watch mode — re-check every 5 seconds
endpulse -c endpoints.yaml -w 5

# Generate a starter config file
endpulse --init
```

## Usage

```
endpulse [OPTIONS] [URLS]...

Options:
  -c, --config PATH       YAML config file
  -n, --repeat INTEGER    Number of rounds  [default: 1]
  -t, --timeout FLOAT     Request timeout in seconds  [default: 10.0]
  --threshold FLOAT       Slow response threshold in ms  [default: 1000.0]
  --method TEXT            HTTP method  [default: GET]
  --concurrency INTEGER   Max concurrent requests  [default: 10]
  -o, --output FORMAT     Output: table|json|markdown|csv  [default: table]
  --json                  Output as JSON (shortcut)
  --fail                  Exit code 1 if any endpoint fails
  -a, --assert TEXT       Assertion (repeatable)
  -w, --watch FLOAT       Watch mode interval in seconds
  --ssl                   Check SSL certificate expiry
  --notify URL            Webhook URL for failure alerts (repeatable)
  --init                  Generate a sample endpoints.yaml
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

# Multiple assertions — fail CI if any assertion fails
endpulse https://api.example.com -a "body_contains:ok" -a "status:200" --fail
```

## SSL Certificate Monitoring

Check SSL certificate expiry alongside health checks:

```bash
# Check health + SSL expiry
endpulse https://api.example.com https://app.example.com --ssl

# SSL check in watch mode — catch expiring certs early
endpulse -c endpoints.yaml --ssl -w 3600
```

The SSL Expiry column shows days remaining. Certificates expiring within 14 days are flagged with `(!)`.

## Webhook Notifications

Get alerted on failures via Slack, Discord, or any webhook:

```bash
# Slack notification on failure
endpulse -c endpoints.yaml --notify https://hooks.slack.com/services/T00/B00/xxx

# Discord notification
endpulse -c endpoints.yaml --notify https://discord.com/api/webhooks/123/abc

# Multiple webhooks
endpulse -c endpoints.yaml \
  --notify https://hooks.slack.com/services/T00/B00/xxx \
  --notify https://example.com/webhook

# Watch mode with alerts — continuous monitoring with notifications
endpulse -c endpoints.yaml -w 30 --notify https://hooks.slack.com/services/T00/B00/xxx
```

Webhook type is auto-detected from the URL. Generic webhooks receive a JSON payload with full results.

You can also configure notifications in the YAML config:

```yaml
notify:
  - https://hooks.slack.com/services/YOUR/WEBHOOK/URL

endpoints:
  - https://api.example.com/health
```

## Output Formats

```bash
# Rich terminal table (default)
endpulse https://api.example.com

# JSON — pipe to jq or monitoring systems
endpulse https://api.example.com --output json

# Markdown — paste into GitHub Actions summary
endpulse -c endpoints.yaml --output markdown >> $GITHUB_STEP_SUMMARY

# CSV — import into spreadsheets or data tools
endpulse -c endpoints.yaml --output csv > results.csv
```

## Config File

Generate a starter config:

```bash
endpulse --init
```

This creates `endpoints.yaml` in your current directory:

```yaml
defaults:
  timeout: 10
  threshold_ms: 1000
  method: GET

notify:
  - https://hooks.slack.com/services/YOUR/WEBHOOK/URL

endpoints:
  - https://your-api.com/health

  - url: https://your-api.com/v2/status
    method: GET
    timeout: 5
    threshold_ms: 500
    assert:
      - "body_contains:ok"
      - "status:200"

  - url: https://your-api.com/webhook
    method: POST
    expected_status: 201
```

```bash
endpulse -c endpoints.yaml --fail
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Health check
  run: |
    pip install endpulse
    endpulse -c endpoints.yaml --fail

# With Markdown summary
- name: Health check with report
  run: |
    pip install endpulse
    endpulse -c endpoints.yaml --output markdown --ssl >> $GITHUB_STEP_SUMMARY
    endpulse -c endpoints.yaml --fail
```

### GitLab CI

```yaml
health_check:
  script:
    - pip install endpulse
    - endpulse -c endpoints.yaml --fail --output json > health-report.json
  artifacts:
    paths:
      - health-report.json
```

The `--fail` flag makes endpulse return exit code 1 when any endpoint is DOWN or fails an assertion — your pipeline stops on unhealthy services.

## Watch Mode

Monitor endpoints continuously:

```bash
# Re-check every 5 seconds
endpulse https://api1.com https://api2.com -w 5

# Watch with failure alerting to Slack
endpulse -c endpoints.yaml -w 30 --fail \
  --notify https://hooks.slack.com/services/T00/B00/xxx
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
