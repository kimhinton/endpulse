# Reddit — r/Python (Showcase flair)

Submit to: https://www.reddit.com/r/Python/submit

## Rules you MUST follow (r/Python 2026 Showcase rules)

- [ ] Post type: text post only (no link post)
- [ ] Flair: "Showcase"
- [ ] Body must contain these three sections in this order: **What My Project Does**, **Target Audience**, **Comparison**
- [ ] Working installable package (PyPI required) — covered ✓
- [ ] Don't post more than once every 30 days about the same project

## Title (pick one — A/B)

**A (feature-led, recommended):**
> endpulse — Multi-endpoint API health checker with assertions, SSL monitoring, and CI exit codes

**B (benefit-led):**
> I built a CLI that replaces your curl-in-a-loop deploy health checks

## Body

```markdown
## What My Project Does

endpulse is a CLI tool that checks multiple API endpoints concurrently and reports their health status in a single command.

Capabilities:
- Async concurrent health checks across 50+ endpoints simultaneously
- Response assertions — validate body content, regex patterns, headers, and status codes directly from CLI flags
- SSL certificate expiry monitoring with `--ssl`
- Watch mode with a live-updating Rich terminal table (`-w 5` re-checks every 5 seconds)
- CI/CD integration — `--fail` returns exit code 1 when any endpoint is down or fails an assertion
- Webhook notifications to Slack, Discord, or generic webhooks on failure
- Multiple output formats: table, JSON, Markdown (for GitHub Actions summaries), CSV
- YAML config files for defining all endpoints, thresholds, and assertions in one place
- GitHub Actions composite action shipped in the repo (uses: kimhinton/endpulse@v0.3.0)

Example:

```bash
pip install endpulse
endpulse https://api.example.com/health https://api.example.com/v2 \
    --ssl --fail -a "body_contains:ok"
```

GitHub: https://github.com/kimhinton/endpulse
PyPI: https://pypi.org/project/endpulse/

## Target Audience

Production use by developers and DevOps engineers who need to:

- Verify staging/production API health after deployments
- Add health-check steps to CI/CD pipelines (GitHub Actions, GitLab CI)
- Monitor SSL certificate expiry without setting up a full monitoring stack
- Replace fragile bash scripts that curl endpoints in a loop and grep for "ok"

It is NOT a load testing tool — it checks health status, not performance under load.

## Comparison

| Tool | Difference from endpulse |
|------|--------------------------|
| **curl / httpie** | Single-endpoint only. No assertions, no watch mode, no concurrent checks. endpulse checks many endpoints at once with pass/fail assertions. |
| **hurl** | Closest competitor. Has assertions and CI support, but uses its own file DSL (not YAML), has no watch mode, and no concurrent multi-endpoint dashboard. |
| **k6 / Artillery** | Load testing tools requiring JavaScript scripts. Overkill for "are these 10 endpoints returning 200?". endpulse is a health checker, not a load tester. |
| **Uptime Kuma / Gatus** | Require deploying and running a server with a web UI. endpulse is zero-infrastructure — `pip install` and run from terminal or CI. |

Built with Python 3.9+, httpx for async HTTP, Rich for terminal output, Click for CLI. MIT licensed, no external service dependencies.
```

## After posting

- First 15 min: reply to every comment, even one-liners — r/Python upvote algorithm weights early engagement
- First 2h: answer technical questions in detail
- Do NOT delete and repost if it flops — 30-day cooldown on the same project
- If flair is wrong, mods will remove — ping modmail politely if that happens
