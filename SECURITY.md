# Security Policy

## Supported Versions

| Version | Supported |
| ------- | :-------: |
| 0.3.x   | ✅        |
| < 0.3   | ❌        |

Only the latest minor version receives security fixes. Please upgrade to `0.3.x` (or later) before reporting vulnerabilities in older versions.

## Reporting a Vulnerability

If you discover a security vulnerability in endpulse, **please report it privately** — do not open a public issue.

Preferred channel:
- [GitHub private vulnerability reporting](https://github.com/kimhinton/endpulse/security/advisories/new)

Alternative:
- Email the maintainer at `kim.hinton00@gmail.com` with the subject line `endpulse security:`.

Please include:
- The endpulse version and Python version you tested.
- A minimal reproduction (CLI command or YAML config).
- The impact (what an attacker could do).
- Any suggested mitigation or patch, if you have one.

## Response timeline

| Step | Target |
|------|--------|
| Acknowledgement | Within 72 hours |
| Initial assessment | Within 7 days |
| Fix or planned timeline | Within 14 days for confirmed issues |
| Public advisory + credit | After a fix ships, with reporter credit (opt-in) |

## Scope

In scope:
- endpulse Python package and its CLI.
- The `action.yml` GitHub Actions composite action.
- Documentation or configuration templates that could mislead users into insecure setups.

Out of scope:
- Vulnerabilities in upstream dependencies (`httpx`, `click`, `rich`, `pyyaml`) — report those to the respective projects.
- Denial-of-service against a user's own endpoints (endpulse is a client tool; aggressive usage settings are user-controlled).
- Issues requiring privileged local access or modified source.

## Good-faith safe harbor

We will not pursue legal action against researchers who:
- Report in good faith through the private channels above.
- Avoid accessing, modifying, or exfiltrating data that isn't their own during testing.
- Give us a reasonable window to fix before public disclosure.
