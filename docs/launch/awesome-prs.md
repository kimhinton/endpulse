# awesome-list PR campaign

Long-tail SEO. Each PR is cheap (~5 min), collectively brings consistent referrals months after launch.

## Submission order (highest acceptance rate first)

1. **ml-tooling/best-of-python-dev** — automated acceptance via YAML config, fastest turnaround
2. **agarrharr/awesome-cli-apps** — CLI-specific, moderate acceptance rate
3. **dastergon/awesome-sre** — smaller, more focused, quick reviews
4. **wmariuss/awesome-devops** — medium-sized, picky about quality
5. **vinta/awesome-python** — largest, lowest acceptance rate, longest review — submit last

## Per-repo templates (ready to paste)

### 1. ml-tooling/best-of-python-dev

Repo: https://github.com/ml-tooling/best-of-python-dev

This list is auto-generated from `projects.yaml`. PR against that file.

Add under the appropriate category (`Code Quality` or create a new `Testing & Health` section if missing):

```yaml
- name: endpulse
  github_id: kimhinton/endpulse
  pypi_id: endpulse
  labels:
    - "devops"
    - "testing"
  description: "CLI for multi-endpoint API health checks with assertions, SSL monitoring, watch mode, and CI exit codes."
```

PR title: `Add endpulse to projects.yaml`
PR body: One sentence — "Adds endpulse, a CLI for API endpoint health checks with assertions and SSL monitoring."

### 2. agarrharr/awesome-cli-apps

Repo: https://github.com/agarrharr/awesome-cli-apps

Add under **Development → Testing / API Clients** (match the closest existing section — read the README for current categories):

```markdown
- [endpulse](https://github.com/kimhinton/endpulse) - Multi-endpoint API health checks with assertions, SSL monitoring, watch mode, and CI exit codes.
```

PR title: `Add endpulse — API health-check CLI`
PR body:
```
Adds endpulse, a Python CLI for multi-endpoint API health checking with response assertions, SSL certificate monitoring, watch mode, and CI/CD integration.

- GitHub: https://github.com/kimhinton/endpulse
- PyPI: https://pypi.org/project/endpulse/
- License: MIT

Follows the list's requirements: open-source, actively maintained, installable in one command.
```

### 3. dastergon/awesome-sre

Repo: https://github.com/dastergon/awesome-sre

Add under **Tools → Monitoring / Observability** (or the nearest matching section):

```markdown
- [endpulse](https://github.com/kimhinton/endpulse) - CLI for synthetic API health checks with assertions, SSL expiry monitoring, webhook alerts, and CI exit codes.
```

PR title: `Add endpulse under Monitoring`

### 4. wmariuss/awesome-devops

Repo: https://github.com/wmariuss/awesome-devops

Add under **Testing → API Testing** or **Monitoring**:

```markdown
- [endpulse](https://github.com/kimhinton/endpulse) - Multi-endpoint API health-check CLI with response assertions, SSL monitoring, watch mode, and webhook alerts. Zero-infrastructure — pip install.
```

PR title: `Add endpulse to API Testing section`

### 5. vinta/awesome-python

Repo: https://github.com/vinta/awesome-python

This list is curated strictly. Requirements (current as of 2026-04-21):
- Project must have > 500 GitHub stars [if this is enforced — verify in CONTRIBUTING.md before submitting]
- Must be actively maintained
- Must have tests
- Must have docs

Submit ONLY after hitting the star threshold. For now, leave this one queued.

Template when ready:

```markdown
- [endpulse](https://github.com/kimhinton/endpulse) - Multi-endpoint API health checker with assertions, SSL monitoring, and CI exit codes.
```

Target section: **Testing** or **HTTP Clients**.

## Secondary candidates (smaller lists, higher acceptance)

Submit these once the primary list PRs are out:

| Repo | Section target |
|------|----------------|
| https://github.com/alebcay/awesome-shell | CLI Utilities |
| https://github.com/Kickball/awesome-selfhosted | Monitoring (borderline — endpulse isn't self-hosted per se) |
| https://github.com/markets/awesome-ruby | N/A (skip) |
| https://github.com/uhub/awesome-python | Testing |
| https://github.com/MunGell/awesome-for-beginners | N/A — endpulse isn't beginner-targeted |

Search GitHub for `awesome-cli awesome-python awesome-devops awesome-sre awesome-monitoring awesome-http awesome-api-testing` — each is worth 30 seconds of looking to see if the scope fits.

## PR hygiene

- Read each list's CONTRIBUTING.md before opening a PR. Most have a strict line format and will auto-reject formatting drift
- Keep PR descriptions ≤ 3 sentences — maintainers skim
- If an existing similar tool is already listed, reference it: "complements X by adding Y"
- Never argue if rejected — move on. awesome-list rejections are often taste-based
- After acceptance: note the referrer in your GitHub traffic page and share the final PR on your Twitter thread as social proof

## Tracking

Copy this table to your local notes after submitting:

| Date | Repo | PR URL | Status | Notes |
|------|------|--------|--------|-------|
|      |      |        |        |       |
