# Contributing to endpulse

Thanks for considering a contribution.

## Setup

```bash
git clone https://github.com/kimhinton/endpulse.git
cd endpulse
pip install -e ".[dev]"
```

## Development Workflow

```bash
# Run tests
pytest -v

# Run tests with coverage
pytest --cov=endpulse --cov-report=term-missing

# Lint
ruff check endpulse/ tests/

# Type check
mypy endpulse/
```

## Project Structure

```
endpulse/
  cli.py          # Click CLI entry point
  checker.py      # Async HTTP endpoint checking
  config.py       # YAML config loading and init template
  models.py       # Data models (EndpointConfig, EndpointResult, SSLInfo)
  reporter.py     # Output formatting (table, JSON, Markdown, CSV)
  ssl_checker.py  # SSL certificate expiry checking
  notifier.py     # Webhook notifications (Slack, Discord, generic)
tests/
  test_*.py       # Test files matching each module
```

## Pull Requests

1. Fork the repo and create a feature branch
2. Write tests for new functionality
3. Ensure all checks pass (`pytest`, `ruff`, `mypy`)
4. Submit a PR with a clear description

## Reporting Issues

Open an issue at [github.com/kimhinton/endpulse/issues](https://github.com/kimhinton/endpulse/issues) with:

- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
