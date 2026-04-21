# Dev.to / Hashnode — long-form article

Publish to: https://dev.to/new (canonical URL back to your GitHub Pages site if you cross-post)

## Frontmatter

```yaml
title: "I built a CLI that replaces your curl health-check scripts"
published: true
description: "endpulse is a small Python CLI for multi-endpoint API health checks with assertions, SSL monitoring, and CI exit codes. Here's why I built it and how it fits between curl and k6."
tags: python, devops, opensource, cli
cover_image: https://kimhinton.github.io/endpulse/og-image.png
canonical_url: https://kimhinton.github.io/endpulse/
```

## Tag strategy

Pick 4 (Dev.to limit):
1. `python` — large audience, good discovery
2. `devops` — right persona
3. `opensource` — trend tag
4. `cli` — small but targeted

Avoid `webdev` — too broad, dilutes clicks.

## Article body

```markdown
Every deployment pipeline I've worked on has the same pattern: a bash script that curls a list of endpoints, greps for "ok" in the response, and exits 1 if something fails. It works, until it doesn't.

Here's what mine looked like, circa 2023:

```bash
#!/bin/bash
set -e
for url in "${ENDPOINTS[@]}"; do
  response=$(curl -s -o /dev/null -w "%{http_code}" "$url") || exit 1
  if [ "$response" != "200" ]; then
    echo "FAIL: $url returned $response"
    exit 1
  fi
done
```

That works for a week. Then:

- You want to check response body, not just status code → more `curl` + `grep` + escaping hell
- You want to check SSL expiry → you remember `openssl s_client`, then forget the flag next time
- You want concurrent checks because serial is slow for 20 endpoints → bash subshells, wait, traps
- You want to fail CI on slow responses → you parse `curl -w "%{time_total}"` and compare with `bc`
- You want a Slack alert → curl to a webhook URL, but only if status!=200 or response body doesn't contain the right string

Every incremental feature makes the script more fragile. The bash becomes unmaintainable faster than you can replace it.

So I built endpulse — a small Python CLI that takes that ball of string and gives it a proper shape.

## What endpulse does

One command, multiple endpoints, structured output:

```bash
pip install endpulse
endpulse https://api.example.com/health https://api.example.com/v2 \
    --ssl --fail -a "body_contains:ok" -a "status:200"
```

Output:

```
                         Endpoint Health Report
+---------------------------------------------------------------+
| URL                           | Status | Code | Time(ms) | SSL |
|-------------------------------|--------|------|----------|-----|
| api.example.com/health        |   UP   |  200 |    42.5  | 89d |
| api.example.com/v2            |   UP   |  200 |   118.3  | 89d |
+---------------------------------------------------------------+

2/2 endpoints up  |  avg response: 80.4ms
```

Exit code 1 if anything fails (thanks to `--fail`) — so CI just works.

## Features that replaced my bash scripts

### Response assertions from CLI flags

No more `curl | jq | grep`. Four assertion types, all from flags:

```bash
endpulse https://api.example.com \
    -a "body_contains:ok" \
    -a "body_regex:version.*\d+\.\d+" \
    -a "header_contains:content-type:json" \
    -a "status:200"
```

Pass → green UP. Fail → red DOWN + which assertion failed. Exit 1 with `--fail`.

### SSL certificate monitoring

`--ssl` adds a column with days until cert expiry. Certs expiring in under 14 days get a `(!)` marker.

```bash
endpulse https://api.example.com --ssl
```

This replaces the line of `openssl s_client | openssl x509 -noout -dates` I could never remember.

### Watch mode — live on-call terminal

`-w 5` re-checks every 5 seconds with a live-updating Rich table:

```bash
endpulse -c endpoints.yaml -w 5 --ssl
```

Useful when you're debugging an incident and want a live view without opening Grafana.

### Webhook alerts

Generic webhook + auto-detection for Slack and Discord:

```bash
endpulse -c endpoints.yaml --notify https://hooks.slack.com/services/.../...
```

### CI-friendly output

JSON, Markdown, CSV — pipe them wherever:

```bash
# GitHub Actions job summary
endpulse -c endpoints.yaml --output markdown >> $GITHUB_STEP_SUMMARY

# Feed into another tool
endpulse -c endpoints.yaml --output json | jq '.[] | select(.status=="DOWN")'
```

### YAML config for repeatable setups

```yaml
defaults:
  timeout: 10
  threshold_ms: 500

notify:
  - https://hooks.slack.com/services/YOUR/WEBHOOK/URL

endpoints:
  - url: https://api.example.com/health
    assert:
      - body_contains: ok
      - status: 200
  - url: https://api.example.com/v2/ping
    assert:
      - body_regex: 'version.*\d+\.\d+'
```

Generate a starter with `endpulse --init`.

### GitHub Actions composite action

Drop this in a workflow:

```yaml
- uses: kimhinton/endpulse@v0.3.0
  with:
    config: endpoints.yaml
    fail-on-error: true
```

## Where endpulse fits

This is the part where I tell you what endpulse *isn't*, because tool positioning matters more than feature lists.

| Tool | What it's for | Is endpulse a replacement? |
|------|---------------|----------------------------|
| **curl** | Any one HTTP call | Yes, for the "check many endpoints" case |
| **httpie** | Human-friendly one-off requests | Yes, for the "check many endpoints" case |
| **hurl** | HTTP flow testing with its own DSL | No — different scope. hurl is for test cases, endpulse for health checks |
| **k6 / Artillery** | Load testing with JS scripts | No — different problem. endpulse doesn't simulate load |
| **Uptime Kuma / Gatus** | Continuous uptime monitoring with web UI | No — those need a server. endpulse is zero-infrastructure |
| **Pingdom / StatusCake** | SaaS uptime monitoring | No — endpulse runs on your machine or CI |

The specific niche endpulse fills: **post-deploy checks, CI health gates, on-call terminal checks, cron-driven synthetic smoke tests**. Anywhere you'd write a bash script today.

## Try it

```bash
pip install endpulse
endpulse --init  # generates endpoints.yaml
endpulse -c endpoints.yaml --ssl --fail
```

- GitHub (star if useful): https://github.com/kimhinton/endpulse
- PyPI: https://pypi.org/project/endpulse/
- Docs: https://kimhinton.github.io/endpulse/

MIT licensed. Python 3.9+. Cross-platform (Linux, macOS, Windows). Built on httpx, Click, and Rich — no external services required.

I'd love feedback, especially:
- Is `body_contains:ok` readable, or should it be a cleaner DSL like `--assert body contains "ok"`?
- What synthetic-check output format would best plug into your existing alerting?

If you find a bug, issues are [here](https://github.com/kimhinton/endpulse/issues). PRs welcome.
```

## Canonical URL

If you cross-post to Hashnode or your own blog, set `canonical_url` to the **first** URL published — pick ONE as the canonical to avoid duplicate content penalties.

If GitHub Pages is canonical, the URL is `https://kimhinton.github.io/endpulse/` (you'd need to publish a blog there separately — otherwise, Dev.to is the canonical).

## After publishing

- Dev.to sends a weekly digest to tag subscribers — `#python` and `#devops` subscribers will see it
- Tweet a link pointing to the Dev.to post, NOT directly to GitHub — Dev.to backlinks compound
- Reply to every comment — Dev.to promotes high-engagement posts to front page
