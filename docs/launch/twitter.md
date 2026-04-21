# Twitter / X — launch thread

## Thread (copy each tweet into the X composer)

### 1/7 (hook)

```
Shipped a small Python CLI I built for a problem I kept solving the wrong way:
"is this list of API endpoints up, healthy, and returning what it should?"

meet endpulse — a single command, N endpoints, structured pass/fail.

pip install endpulse

🧵
```

### 2/7 (the problem)

```
Every deploy pipeline I've worked on ends up with:

for url in "${URLS[@]}"; do
  curl -s ... | grep "ok"  || exit 1
done

This works until you want assertions, SSL expiry, watch mode, webhooks, or CI-friendly output.
Then the bash grows a beard.
```

### 3/7 (demo — attach docs/og-image.png OR docs/demo.png here)

```
endpulse api1 api2 api3 --ssl --fail -a "body_contains:ok"

                    Endpoint Health Report
URL                          Status  Code  Time   SSL
api.example.com/health         UP     200   42ms  89d
api.example.com/v2             UP     200   118ms 89d
api.example.com/slow          SLOW    200   1.8s  89d

exit 0 (or 1 if you used --fail)
```
(Attach image: `docs/demo.png`)

### 4/7 (what's inside)

```
In one CLI:

• async concurrent checks (httpx)
• CLI-flag assertions: body, regex, headers, status
• --ssl  certificate expiry monitoring
• -w N   watch mode (live Rich terminal table)
• --fail CI exit codes
• --notify Slack/Discord/generic webhook
• table / json / markdown / csv output
• YAML config  +  --init starter

zero external services.
```

### 5/7 (positioning)

```
What endpulse is NOT:

• not a load tester → use k6 / Artillery
• not an always-on uptime monitor → use Kuma / Gatus / Pingdom
• not HTTP-flow testing → use hurl

What it IS:
the thing you run in CI, on-call terminals, cron, k8s initContainers.

the gap curl-in-a-loop keeps growing into.
```

### 6/7 (GitHub Actions plug)

```
bonus: there's a Composite Action in the repo.

drop this in a workflow:

- uses: kimhinton/endpulse@v0.3.0
  with:
    config: endpoints.yaml
    fail-on-error: true

and every deploy gets a health-gate for free.
```

### 7/7 (CTA)

```
MIT licensed. Python 3.9+. Linux / macOS / Windows.

⭐ https://github.com/kimhinton/endpulse
📦 https://pypi.org/project/endpulse/
📖 https://kimhinton.github.io/endpulse/

would love feedback — especially on the assertion DSL and what I'm missing from your CI pipeline.
```

## Image strategy

- Tweet 3: attach `docs/demo.png` (1600×900)
- Tweet 7 (optional): attach `docs/og-image.png` (1200×630) for the CTA card

Twitter auto-crops 16:9 — the demo PNG is designed for that aspect.

## Posting notes

- Post all 7 tweets as one native thread — do NOT paste them one by one with time gaps (kills the algorithm)
- X/Twitter downranks tweets with more than 3 links — keep links in tweet 7 only
- The first tweet determines reach. Iterate on it if tweet 1 flops within 30 min — delete the whole thread and re-post with a new hook
- Don't tag big accounts asking for RTs — it looks desperate and doesn't work
- Reply to EVERY quote-tweet and reply in the first 4 hours

## After posting

- Pin the thread to your profile for 1 week
- Retweet tweet 1 (just that one) 24h later — catches a different timezone
- If any tweet gets 50+ likes, quote-tweet it from the repo's future updates as social proof
