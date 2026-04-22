# endpulse GitHub Topics Manifest

**Last updated**: 2026-04-22
**Total topics**: 20 (GitHub maximum)
**Update API**: `PUT /repos/kimhinton/endpulse/topics`

---

## Current topics (20)

```
api, cli, devops, health-check, monitoring, python, ssl, webhook,
api-monitoring, ci-cd, command-line-tool, developer-tools, http-client,
observability, sre, synthetic-monitoring, uptime-monitoring,
asyncio, endpoint, certificate-monitoring
```

---

## Added in this batch (2026-04-22)

3 topics added. All 17 existing topics preserved.

| Topic | Rationale |
|-------|-----------|
| `asyncio` | endpulse core is an asyncio-based async endpoint/TLS monitor. Maps to an actual Python runtime feature. |
| `endpoint` | Primary monitoring target domain. Core keyword that directly matches the repo name (`endpulse`). |
| `certificate-monitoring` | TLS certificate expiry detection feature. Specific differentiation versus the single `ssl` tag. |

---

## Verification

```bash
# Applied update command (executed)
gh api -X PUT repos/kimhinton/endpulse/topics \
  -f 'names[]=api' -f 'names[]=cli' -f 'names[]=devops' \
  -f 'names[]=health-check' -f 'names[]=monitoring' -f 'names[]=python' \
  -f 'names[]=ssl' -f 'names[]=webhook' -f 'names[]=api-monitoring' \
  -f 'names[]=ci-cd' -f 'names[]=command-line-tool' -f 'names[]=developer-tools' \
  -f 'names[]=http-client' -f 'names[]=observability' -f 'names[]=sre' \
  -f 'names[]=synthetic-monitoring' -f 'names[]=uptime-monitoring' \
  -f 'names[]=asyncio' -f 'names[]=endpoint' -f 'names[]=certificate-monitoring'
```

**Result verification**
- [x] API response `names` array confirmed to contain all 20 topics (verified 2026-04-22)
- [x] 3 new topics (`asyncio`, `endpoint`, `certificate-monitoring`) confirmed added
- [x] All 17 pre-existing topics preserved

---

## Change history

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-04-22 | +asyncio, +endpoint, +certificate-monitoring (17 → 20) | 2026-04-21 meeting — not restricted by conditional commitments (clear runtime feature match) |
