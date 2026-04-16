# Launch Post Drafts

> These are ready-to-post drafts. Copy and paste to each platform.

---

## Reddit r/Python (Show & Tell)

**Title:** endpulse — Multi-endpoint API health checker with assertions, SSL monitoring, and CI exit codes

**Body:**

I built a CLI tool that fills the gap between one-shot HTTP clients (httpie, curl) and heavy monitoring infrastructure (Uptime Kuma, Datadog).

**What it does:**
- Check multiple API endpoints concurrently in one command
- Assert response body, headers, and status codes
- Monitor SSL certificate expiry
- Watch mode with a live-updating terminal table
- `--fail` exit code for CI/CD pipelines
- Slack/Discord/webhook alerts on failures
- Output as table, JSON, Markdown, or CSV

**Quick example:**

```bash
pip install endpulse
endpulse https://api.example.com/health https://api.example.com/v2 --ssl --fail
```

**Why I built this:** I was tired of writing bash scripts with curl loops to check staging endpoints after deploys. k6 is overkill for "are these 10 endpoints returning 200?", and Uptime Kuma requires running a server. I wanted `pip install` + one command.

**Tech:** Python 3.9+, async with httpx, Rich for terminal output. No external service dependencies.

GitHub: https://github.com/kimhinton/endpulse
PyPI: https://pypi.org/project/endpulse/

Would love feedback on the CLI design and any features you'd want to see next.

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
