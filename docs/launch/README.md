# Launch playbook

Ready-to-execute distribution plan for endpulse. Go channel-by-channel, hit the publish button, come back and tick the checkbox.

> **Why this file exists:** A CLI that nobody ever hears about does not get stars. The code is done. What's left is *distribution*, and distribution is a checklist, not a mystery.

## Recommended order (fastest to slowest signal)

1. **Day 0 (launch day)** — GitHub polish (this PR merged) + Hacker News Show HN
2. **Day 0 +2h** — Reddit r/Python (Showcase) + r/devops
3. **Day 1** — Dev.to / Hashnode blog post
4. **Day 1–2** — Twitter/X thread
5. **Day 2** — Product Hunt launch
6. **Day 3–7** — awesome-list PRs (incremental)

## Optimal posting windows

| Platform | Best day | Best window (local user time) | Why |
|----------|----------|-------------------------------|-----|
| Hacker News | Tue / Wed / Thu | 07:00–10:00 ET (US morning) | Largest US dev audience waking up |
| Reddit r/Python | Mon / Tue / Wed | 09:00–13:00 ET | Weekday active subscribers |
| Reddit r/devops | Mon / Tue | 09:00–12:00 ET | Workday DevOps browsing |
| Dev.to | Tue / Wed | 10:00–14:00 ET | Publisher window, then indexed |
| Product Hunt | Tue / Wed / Thu | 00:01 PT (launch timer) | PH's 24h scoring cycle starts at midnight PT |
| Twitter/X | Tue / Wed | 09:00–11:00 ET | Dev audience morning scroll |

Avoid weekends and US holidays — dev traffic collapses.

## Pre-flight checklist (run before ANY post)

- [ ] `docs/og-image.png` renders in debugger: https://www.opengraph.xyz/url/https%3A%2F%2Fkimhinton.github.io%2Fendpulse%2F
- [ ] Twitter card validator shows large summary card: https://cards-dev.twitter.com/validator
- [ ] GitHub repo Settings → Social preview uploaded (docs/og-image.png, manual step)
- [ ] PyPI page shows README properly rendered
- [ ] CI badge green on README
- [ ] `pip install endpulse` works in a clean venv
- [ ] At least one recent commit within 24h (GitHub trending signal)

## Per-channel files

| File | Channel | Notes |
|------|---------|-------|
| [hn.md](hn.md) | Hacker News (Show HN) | Most important single channel. Title A/B included. |
| [reddit-python.md](reddit-python.md) | r/Python Showcase | Strict 3-section format. |
| [reddit-devops.md](reddit-devops.md) | r/devops | Self-promo rules apply. |
| [reddit-sre.md](reddit-sre.md) | r/sre | Smaller sub, more technical. |
| [devto.md](devto.md) | Dev.to / Hashnode | Long-form. Drives search over time. |
| [twitter.md](twitter.md) | Twitter / X | 6–7 tweet thread. |
| [producthunt.md](producthunt.md) | Product Hunt | Separate day. |
| [awesome-prs.md](awesome-prs.md) | awesome-list PRs | Long-tail SEO. Each PR is cheap. |
| [github-topics.md](github-topics.md) | Repo topic optimization | Free discoverability. |

## What to do AFTER posting

| Hour +1 | Reply to every comment. Even "thanks" matters for HN ranking. |
| Hour +4 | Check https://news.ycombinator.com/newest for your submission. If buried, post a single context comment (not a bump). |
| Hour +24 | Tweet screenshot of the thread. Don't ask for upvotes — it triggers penalties. |
| Day +2 | Note which channel drove stars (GitHub insights). Double down on winner. |

## Anti-patterns to avoid

- **Don't** post the same title on multiple subs on the same day — spam filter.
- **Don't** ask for upvotes in the thread. HN and Reddit auto-detect and penalize.
- **Don't** submit to HN via alt accounts. The penalty is permanent shadowban.
- **Don't** DM people asking to star — GitHub staff flag coordinated starring.
- **Don't** launch with 0 tests or a broken CI badge. Devs click through and bounce.
- **Don't** edit the post title after submission (HN allows 2h window — use it once if needed, not iteratively).
