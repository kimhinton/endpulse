# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-04-16

### Added
- **SSL certificate monitoring** — `--ssl` flag checks certificate expiry for HTTPS endpoints
- **Webhook notifications** — `--notify` sends alerts to Slack, Discord, or generic webhooks on failure
- **Multiple output formats** — `--output markdown|csv|json|table` for CI reports and data export
- **Config generator** — `--init` creates a starter `endpoints.yaml` in the current directory
- **YAML notification config** — `notify:` key in config file for persistent webhook setup
- **GitHub Actions composite action** — use `kimhinton/endpulse@v0.3.0` directly in workflows
- SSL expiry column in terminal table output
- SSL info in JSON output
- New tests for SSL, notifications, output formats (47 total)

### Changed
- README rewritten with feature comparison table, CI/CD examples, and output format docs
- CONTRIBUTING.md updated with project structure reference

## [0.2.0] - 2026-04-16

### Added
- **Response assertions** — `body_contains`, `body_regex`, `header_contains`, `status` checks
- **Watch mode** — `-w` flag for continuous monitoring with live-updating terminal table
- **CI/CD exit codes** — `--fail` flag returns exit code 1 on any failure
- Assertion support in YAML config via `assert:` key
- Multiple assertion types combinable per endpoint

## [0.1.0] - 2026-04-16

### Added
- Initial release
- Async concurrent endpoint health checking with httpx
- YAML config file support with defaults
- Rich terminal table output
- JSON output format
- Configurable timeout, threshold, concurrency, and HTTP method
- CI pipeline with GitHub Actions (Linux, macOS, Windows)
- Cross-platform support (Python 3.9+)

[0.3.0]: https://github.com/kimhinton/endpulse/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/kimhinton/endpulse/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kimhinton/endpulse/releases/tag/v0.1.0
