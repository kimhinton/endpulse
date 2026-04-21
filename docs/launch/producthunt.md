# Product Hunt — launch

Launch at: https://www.producthunt.com/posts/new

## Launch-day constraints

- PH ranking runs on a 24-hour cycle starting at **00:01 Pacific Time**
- Scheduling lets you pre-fill; actual vote collection begins at PT midnight
- Launch Tuesday / Wednesday / Thursday for best weekday dev traffic
- You need at least one screenshot/video asset to submit

## Fields

**Name:** endpulse

**Tagline** (60 char max — currently uses 58):
> Multi-endpoint API health checks in one CLI command

Alternate taglines (pick whichever tests best):
- "Zero-infra CLI for post-deploy API health gates" (49)
- "The CLI that replaces your curl health-check scripts" (52)
- "API health checks with assertions, SSL, and CI exit codes" (59)

**Topics:** Developer Tools, Open Source, DevOps Tools, Command Line Apps

**Thumbnail:** `docs/icon-512.png`

**Gallery images (recommended 4):**
1. `docs/og-image.png` — hero/social card
2. `docs/demo.png` — terminal output
3. Screenshot of GitHub Actions integration running in a real workflow
4. Screenshot of watch mode in action OR a Slack alert payload

**First video (optional but +ranking):** Record a 20-second asciinema of running `endpulse --init && endpulse -c endpoints.yaml --ssl -w 5` — convert to MP4 with svg-term-cli or similar.

**Maker comment (pin on launch):**

```
Hey Product Hunt 👋 Kim here, maker of endpulse.

I kept writing the same bash script for every project — curl a list of API endpoints, grep for "ok", exit 1 if something fails. It works until you want assertions, SSL monitoring, watch mode, or webhooks. Then the bash becomes a maintenance nightmare.

endpulse is that bash script grown up:

• One command, N endpoints, concurrent checks
• CLI-flag response assertions (body, regex, headers, status)
• SSL cert expiry column (--ssl)
• Watch mode with live Rich terminal table (-w 5)
• Webhook alerts to Slack/Discord (--notify)
• Table / JSON / Markdown / CSV output — CI ready
• GitHub Actions composite action included

It sits between httpie (one endpoint) and k6 (load testing). If you've ever curl'd a health endpoint in a bash loop, this is for you.

pip install endpulse

MIT, Python 3.9+, cross-platform, zero external services needed.

Would especially love:
1. Feedback on the assertion syntax — is CLI-flag form (-a "body_contains:ok") readable, or should it be structured differently?
2. Which CI integration slot is missing? GitLab? CircleCI? BuildKite?

Full docs: https://kimhinton.github.io/endpulse/
GitHub: https://github.com/kimhinton/endpulse

Thanks for taking a look!
```

## Pre-launch checklist (run the day BEFORE)

- [ ] Product Hunt account is NOT brand-new (older accounts get more reach)
- [ ] Profile has an avatar and bio (low-effort accounts get filtered)
- [ ] Have at least 5 PH supporters who will hunt + upvote in the first hour (email them the night before — not during launch)
- [ ] All gallery images uploaded and ordered
- [ ] First comment pre-written
- [ ] Launch scheduled for Tue/Wed/Thu

## During launch day

- 00:01 PT — submission goes live. Post the first comment immediately
- Hour +1 — share on Twitter (link to PH page, NOT GitHub)
- Hour +2 — share in your company Slack / personal network (people with PH accounts only — upvotes from non-PH users don't count)
- Hour +4 — reply to every comment
- Hour +12 — mid-day push: Reddit or HN crowd may have already seen; don't cross-post the PH URL
- Hour +20 — final push on Twitter with "last 4 hours on PH"
- Hour +24 — archive thumbnail of the final rank for future social proof

## Do NOT

- Do NOT ask for upvotes in the first comment ("please upvote" triggers shadow-penalty)
- Do NOT trade upvotes in rings or Discord servers — PH staff actively removes these
- Do NOT post the same pitch copy to HN the same week — PH and HN share a significant audience overlap
