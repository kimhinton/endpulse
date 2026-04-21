# Reddit — r/devops

Submit to: https://www.reddit.com/r/devops/submit

## Rules (r/devops)

- [ ] No blog-spam / affiliate links
- [ ] Self-promotion allowed if substantive (9:1 rule — 9 other comments for every 1 self-promo)
- [ ] Prefer text post with context over bare link
- [ ] Read the pinned "Community wiki" for current rules before posting

## Title

> endpulse — Zero-infrastructure CLI for post-deploy API health checks (OSS, Python)

## Body

```markdown
Sharing a small OSS tool I built for a problem I keep running into: every deploy pipeline ends up with a `for url in ...; do curl` bash script that works until it doesn't.

**endpulse** is a CLI that replaces that with one command, and it's built specifically for the CI/post-deploy checkpoint, not continuous monitoring.

What it does that `curl | grep` doesn't:

- Concurrent checks of 50+ endpoints in one invocation (async httpx)
- Response assertions directly from CLI flags — `body_contains`, `body_regex`, `header_contains`, `status`
- `--fail` returns exit code 1 if anything fails, so CI just works
- SSL cert expiry column with `--ssl` (heads up on the 14-day cliff)
- Watch mode with a live-updating Rich terminal table for incident response
- Webhook alerts (Slack / Discord / generic JSON) without extra infra
- Markdown output you can pipe into GitHub Actions job summaries

GitHub Actions example — drop this in a workflow:

```yaml
- uses: kimhinton/endpulse@v0.3.0
  with:
    config: endpoints.yaml
    fail-on-error: true
```

YAML config:

```yaml
defaults:
  timeout: 10
  threshold_ms: 500
notify:
  - https://hooks.slack.com/services/YOUR/WEBHOOK
endpoints:
  - url: https://api.example.com/health
    assert:
      - body_contains: ok
      - status: 200
  - url: https://api.example.com/v2/ping
```

**What it isn't:**
- Not a load tester (use k6)
- Not an always-on uptime monitor (use Kuma/Gatus/Pingdom)
- Not HTTP flow testing (use hurl)

It's specifically the thing you run in CI and on-call terminals.

MIT. Python 3.9+. No external services needed.

- GitHub: https://github.com/kimhinton/endpulse
- PyPI: https://pypi.org/project/endpulse/
- Docs: https://kimhinton.github.io/endpulse/

Feedback welcome — particularly on the assertion syntax and what to name things in a YAML that isn't already overloaded by k6 or hurl.
```

## Notes

- r/devops tolerates self-promo but hates marketing fluff. Keep the body dense with code, configs, and specific comparisons
- Don't post on Friday — r/devops traffic drops hard on weekends
- Check if any identical-topic post appeared in the last 7 days — mods will remove duplicates
