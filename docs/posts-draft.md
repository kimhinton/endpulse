# Launch Post Drafts

> These are ready-to-post drafts. Copy and paste to each platform.

---

## Reddit r/Python (Showcase flair, text post)

> Rules: Must use "Showcase" flair. Must be text post. Must include 3 required sections.

**Title:** endpulse — Multi-endpoint API health checker with assertions, SSL monitoring, and CI exit codes

**Body:**

## What My Project Does

endpulse is a CLI tool that checks multiple API endpoints concurrently and reports their health status in a single command. It supports:

- Async concurrent health checks across 50+ endpoints simultaneously
- Response assertions — validate body content, regex patterns, headers, and status codes directly from CLI flags
- SSL certificate expiry monitoring with `--ssl`
- Watch mode with a live-updating Rich terminal table (`-w 5` re-checks every 5 seconds)
- CI/CD integration — `--fail` returns exit code 1 when any endpoint is down or fails an assertion
- Webhook notifications to Slack, Discord, or generic webhooks on failure
- Multiple output formats: table, JSON, Markdown (for GitHub Actions summaries), CSV
- YAML config files for defining all endpoints, thresholds, and assertions in one place

```bash
pip install endpulse
endpulse https://api.example.com/health https://api.example.com/v2 --ssl --fail -a "body_contains:ok"
```

GitHub: https://github.com/kimhinton/endpulse
PyPI: https://pypi.org/project/endpulse/

## Target Audience

This is meant for production use by developers and DevOps engineers who need to:

- Verify staging/production API health after deployments
- Add health-check steps to CI/CD pipelines (GitHub Actions, GitLab CI)
- Monitor SSL certificate expiry without setting up a full monitoring stack
- Replace fragile bash scripts that curl endpoints in a loop and grep for "ok"

It is NOT a load testing tool — it checks health status, not performance under load.

## Comparison

| Tool | Difference from endpulse |
|------|--------------------------|
| **curl / httpie** | Single-endpoint only. No assertions, no watch mode, no concurrent checks. endpulse checks many endpoints at once with pass/fail assertions. |
| **hurl** | Closest competitor. Has assertions and CI support, but uses its own file format (not YAML), has no watch mode, and no concurrent multi-endpoint dashboard. |
| **k6 / Artillery** | Load testing tools that require JavaScript scripts. Overkill for "are these 10 endpoints returning 200?". endpulse is a health checker, not a load tester. |
| **Uptime Kuma / Gatus** | Require deploying and running a server with a web UI. endpulse is zero-infrastructure — `pip install` and run from terminal or CI. |

Built with Python 3.9+, httpx for async HTTP, Rich for terminal output, Click for CLI. No external service dependencies.

---

## Hacker News (Show HN)

**Title:** Show HN: Endpulse – Multi-endpoint API health checks with assertions in one CLI command

**URL:** https://github.com/kimhinton/endpulse

**Body (comment):**

Hi HN, I built endpulse because I kept writing the same bash script: curl a list of endpoints, check status codes, parse JSON responses, fail CI if something's wrong.

endpulse replaces that with one command:

    pip install endpulse
    endpulse https://api1.com https://api2.com -a "body_contains:ok" --fail --ssl

Features:
- Async concurrent checks (50+ endpoints in seconds)
- Response assertions (body, headers, status codes) without scripting
- SSL certificate expiry monitoring
- Watch mode for continuous terminal monitoring
- Slack/Discord webhook alerts
- JSON/Markdown/CSV output for CI integration
- YAML config for complex setups

It's positioned between httpie (single endpoint, no assertions) and k6 (load testing, requires JS scripts). Python 3.9+, MIT license, zero external dependencies beyond httpx/click/rich.

GitHub Actions integration works out of the box: https://github.com/kimhinton/endpulse (see action.yml)

---

## Dev.to / Hashnode Blog

**Title:** I built a CLI that replaces your curl health-check scripts

**Tags:** python, cli, devops, monitoring

**Intro paragraph:**

Every deployment pipeline I've worked on has the same pattern: a bash script that curls a list of endpoints, greps for "ok" in the response, and exits 1 if something fails. It works, but it's fragile, hard to maintain, and gives you zero visibility.

I built endpulse to replace those scripts with a proper tool. One pip install, one command, and you get concurrent health checks with assertions, SSL monitoring, and CI exit codes.

[Link to full article if you write it]
