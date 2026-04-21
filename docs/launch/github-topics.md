# GitHub topics — optimization

GitHub allows up to **20 topics** per repo. Current count: 10. Ten slots free — use them.

Topics directly affect:
- `github.com/topics/<topic>` directory listings
- GitHub Explore page surfacing
- Search ranking for repo queries
- "Related repos" sidebar on other repos with shared topics

## Current topics

```
api, async, cli, devops, endpoint, health-check, monitoring, python, ssl, webhook
```

Coverage analysis:
- `api` — huge but generic (competes with 500k+ repos)
- `async` — technical, lower intent
- `cli` — right
- `devops` — right, persona match
- `endpoint` — weak, not a strong search term
- `health-check` — exact intent ✓
- `monitoring` — persona, but endpulse is more "synthetic check" than "monitoring"
- `python` — right
- `ssl` — right
- `webhook` — right (half-feature, half-integration)

Low-value candidates to consider removing:
- `endpoint` (vague, low search volume)
- `async` (implementation detail, not buyer intent)

## Recommended additions (10 slots available)

Priority order — add as many as fit:

1. **`uptime-monitoring`** — high intent, high search volume, on-brand
2. **`api-monitoring`** — direct match to primary use case
3. **`developer-tools`** — broad persona reach
4. **`observability`** — 2025-2026 trend tag, attracts SRE audience
5. **`synthetic-monitoring`** — industry term, lower volume but right audience
6. **`sre`** — persona match, r/sre and SRE weekly will surface
7. **`http-client`** — ecosystem tag, finds users browsing httpx/curl alternatives
8. **`ci-cd`** — CI integration is a core use case
9. **`command-line-tool`** — complements `cli`, catches different searches
10. **`status-page`** — adjacent concept, some overlap in search intent

Also worth considering if you want to trade low-value slots:
- `healthcheck` (no hyphen — different topic from `health-check`; both valid)
- `rest-api`
- `python-cli` (composite tag, some adoption)
- `slack-notifications`
- `discord-notifications`

## Apply topics via gh CLI

Replace current topic set in one command (idempotent):

```bash
gh api --method PUT repos/kimhinton/endpulse/topics \
  -f 'names[]=api' \
  -f 'names[]=api-monitoring' \
  -f 'names[]=ci-cd' \
  -f 'names[]=cli' \
  -f 'names[]=command-line-tool' \
  -f 'names[]=developer-tools' \
  -f 'names[]=devops' \
  -f 'names[]=health-check' \
  -f 'names[]=http-client' \
  -f 'names[]=monitoring' \
  -f 'names[]=observability' \
  -f 'names[]=python' \
  -f 'names[]=sre' \
  -f 'names[]=ssl' \
  -f 'names[]=synthetic-monitoring' \
  -f 'names[]=uptime-monitoring' \
  -f 'names[]=webhook'
```

That's 17 topics. Remaining 3 slots: consider `healthcheck`, `status-page`, `rest-api` depending on future direction.

### Or via Settings UI

Settings → General → Topics. Paste the space-separated list.

## Anti-patterns

- **Don't** keyword-stuff with low-relevance topics (e.g., `framework`, `microservices` unless directly relevant) — GitHub search de-ranks repos with off-topic tags
- **Don't** add topics for technologies you *use* but aren't *about* (e.g., `httpx`, `click`, `rich` — these are deps, not the repo's identity)
- **Don't** add language variants (`python3`, `python-3-9`) — `python` is the canonical one
- **Don't** add `opensource` or `mit-license` — everyone adds these, useless signal

## After applying

- Visit `https://github.com/topics/uptime-monitoring` 24h later — verify your repo appears in the topic page
- GitHub topic pages rank by stars + recency; new repos appear on page 1 briefly even with 0 stars, which drives initial discovery
