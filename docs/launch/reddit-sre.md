# Reddit — r/sre

Submit to: https://www.reddit.com/r/sre/submit

## Why post here

r/sre is smaller (~40k) but denser — readers care about on-call, synthetic checks, SLOs, and automation. Lower traffic, higher quality of feedback.

## Title

> Endpulse — CLI for synthetic health checks with assertions (OSS Python)

## Body

```markdown
SREs — sharing a small OSS CLI for a specific niche: synthetic health checks you can run from anywhere (CI, on-call terminal, cron, k8s initContainer).

The shape of the tool:

- One command → multiple endpoints → structured pass/fail (`--fail` gives CI exit codes)
- Response assertions from CLI flags: `body_contains`, `body_regex`, `header_contains`, `status`
- SSL expiry column alongside health (`--ssl`)
- Watch mode for live on-call terminal: `-w 5`
- Webhook alerts (Slack / Discord / generic JSON) — no extra infra
- YAML config for repeatable defs; `--init` scaffolds one

Synthetic check example — staging smoke test after deploy:

```bash
endpulse -c staging-smoke.yaml --ssl --fail \
    --notify https://hooks.slack.com/services/.../...
```

```yaml
# staging-smoke.yaml
defaults:
  timeout: 5
  threshold_ms: 800
endpoints:
  - url: https://staging.example.com/health
    assert:
      - body_contains: ok
      - status: 200
  - url: https://staging.example.com/readyz
    assert:
      - status: 200
  - url: https://staging.example.com/api/v2/ping
    assert:
      - body_regex: 'version.*\d+\.\d+\.\d+'
```

Scope is deliberately narrow:
- NOT a load tester (k6 / Gatling / Artillery)
- NOT a continuous uptime monitor (Kuma / Gatus / Pingdom / StatusCake)
- NOT HTTP flow testing (hurl)

It's the tool for the gap between `curl --fail-with-body` and a full monitoring stack.

Would love input:
- Is the assertion syntax ergonomic for your scripts?
- Is the SLO use case (e.g. "fail CI if p95 > 500ms over 10 rounds") worth building with `-n 10 --threshold 500`?
- What synthetic-check output format would best integrate with your alerting stack?

GitHub: https://github.com/kimhinton/endpulse
PyPI: https://pypi.org/project/endpulse/
MIT, Python 3.9+.
```
