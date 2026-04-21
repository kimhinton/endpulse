# Hacker News — Show HN

Submit to: https://news.ycombinator.com/submit

## Title (pick one — A/B)

**A (action-led, recommended):**
> Show HN: Endpulse – Multi-endpoint API health checks with assertions in one CLI

**B (problem-led):**
> Show HN: I replaced my curl-in-a-loop health-check bash scripts with a single CLI

**Rules:**
- Max 80 characters
- Start with "Show HN:" (HN convention, unlocks Show page)
- No clickbait, no caps abuse, no emoji — HN mods downrank these

## URL

`https://github.com/kimhinton/endpulse`

(Not the Pages site. HN readers trust GitHub URLs more and the README is richer.)

## First comment (post immediately after submission)

```
Hi HN, I'm the author. endpulse is a small Python CLI I built because every
deploy pipeline I've worked on had the same pattern: a bash script that
curls a list of endpoints, parses output with grep/jq, and exits 1 if
anything looks off. It works, but it's fragile and gives zero visibility.

endpulse replaces that with one command:

    pip install endpulse
    endpulse https://api1.example.com https://api2.example.com \
        --ssl --fail -a "body_contains:ok"

What it does:
  * async concurrent checks (50+ endpoints in seconds)
  * response assertions (body / regex / headers / status) from CLI flags
  * SSL certificate expiry monitoring
  * watch mode with a live-updating Rich terminal table
  * webhook alerts (Slack / Discord / generic) on failures
  * JSON / Markdown / CSV output for CI integration
  * YAML config for repeatable setups

Positioning: it sits between httpie (one endpoint, no assertions) and k6
(load testing, requires JS scripts). It is NOT a load tester. Closest
competitor is hurl, but hurl uses its own DSL and has no watch mode or
concurrent dashboard.

There's also a GitHub Actions composite action in the repo — drop
`uses: kimhinton/endpulse@v0.3.0` in a workflow and health-check on
every deploy.

MIT, Python 3.9+. Would love feedback, especially:
  * assertion syntax — is `body_contains:ok` readable, or should it
    be a cleaner DSL?
  * anything you want that k6/hurl/curl all fail at?

Repo: https://github.com/kimhinton/endpulse
PyPI: https://pypi.org/project/endpulse/
```

## Response playbook (have these ready for the first 2h)

| Likely comment | Your reply |
|----------------|------------|
| "How is this different from hurl?" | "hurl is closer than curl — good call. Two differences: hurl uses its own file DSL, endpulse uses YAML + CLI flags; and endpulse has concurrent multi-endpoint dashboard with watch mode, which hurl doesn't expose. hurl is better for HTTP *test* flows, endpulse for health-check *monitoring*." |
| "Why not just use k6?" | "k6 is a load tester — writing a k6 script just to check 'does this endpoint return 200 with \"ok\" in the body' is overkill. Different mental model: k6 asks 'how does it behave under load', endpulse asks 'is it up'." |
| "What about Uptime Kuma / Gatus?" | "Those are great but require running a server. endpulse is zero-infrastructure — pip install and run from CI or a terminal. If you already have Kuma, keep it; endpulse is for the case where you don't want another service to maintain." |
| "Assertion DSL feels stringly-typed" | "Fair — YAML config has structured `assert:` keys, CLI flags are the shortcut. I'm open to `--assert status=200` style if there's appetite." |
| "Is there a GUI / web dashboard?" | "No, and by design. The gap being filled is CLI/CI. Watch mode is the terminal equivalent of a dashboard." |
| "SSL check — how?" | "Direct TCP socket + `ssl.SSLContext.wrap_socket()`, reads the peer cert's `notAfter`. No external API, no rate limits." |

## Do NOT

- Do NOT reply within 30 seconds of submission — looks automated
- Do NOT ask for upvotes in the thread or anywhere
- Do NOT cross-post within 24h of HN to the same title on Reddit (HN and Reddit share readers; looks farm-y)
- Do NOT argue with downvotes — reply once with evidence, then disengage

## After the launch

- Archive a screenshot of the Show HN page if it ranks top-30 (for your portfolio / Twitter recap)
- Check the GitHub traffic tab — "referring sites" will show which HN comment landed stars
