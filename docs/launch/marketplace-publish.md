# GitHub Actions Marketplace publish

The repo already ships a Composite Action (`action.yml`) that callers use via `uses: kimhinton/endpulse@v0.3.0`. Publishing to the Marketplace adds permanent SEO value: `github.com/marketplace/actions/endpulse` becomes a discovery page for every GitHub Actions user searching "health check" or "api monitoring".

## Pre-flight checklist

Before publishing, verify these are in order (already confirmed as of 2026-04-21):

- [x] Repository is **public**.
- [x] `action.yml` exists at repo root.
- [x] Action has been used at least once (internal CI or a downstream workflow).
- [x] At least one tagged release exists (v0.2.0, v0.3.0).
- [x] `action.yml` has `name`, `description`, `author`, and `branding` (icon + color).
- [ ] `action.yml` `name` is globally unique on GitHub Marketplace — search https://github.com/marketplace?query=endpulse first. If another action is already named "endpulse", either rename or use a specific variant like `endpulse-health-check`.
- [ ] `action.yml` `description` is **≤125 characters** (Marketplace hard limit).
- [ ] `branding.icon` is from the [Feather icon set](https://feathericons.com). Recommended: `activity`, `heart`, `cpu`, or `zap`.
- [ ] `branding.color` is one of: `white`, `yellow`, `blue`, `green`, `orange`, `red`, `purple`, `gray-dark`.

## Publishing steps (manual — ~2 minutes)

1. Go to https://github.com/kimhinton/endpulse/releases
2. Click **"Edit"** on the latest release (`v0.3.0`).
3. Scroll to the section **"Publish this Action to the GitHub Marketplace"**.
4. Check the box `Publish this Action to the GitHub Marketplace`.
5. If this is your first Marketplace submission, accept the **GitHub Marketplace Developer Agreement**.
6. Pick:
   - **Primary category:** `Continuous integration`
   - **Secondary category:** `Monitoring`
7. Click **Update release**.

## After publishing

- The action appears at `https://github.com/marketplace/actions/endpulse` (usually within minutes).
- The Marketplace badge becomes valid and can be re-added to README:

  ```markdown
  [![GitHub Action](https://img.shields.io/badge/Marketplace-GitHub%20Action-blue?logo=github)](https://github.com/marketplace/actions/endpulse)
  ```

- New releases published from now on can opt into "Publish this Action to the Marketplace" with one checkbox.

## Why it matters for discovery

- Permanent SEO page on `github.com/marketplace` — indexed by Google.
- Appears in Marketplace search for "health check", "monitoring", "api", "uptime", "ssl".
- Marketplace entries appear in the Actions tab's "Search Marketplace for actions" sidebar for every workflow author.
- awesome-github-actions lists scrape Marketplace — publishing automatically qualifies the project for those curated lists.

## Common issues

- **"Name already taken"** — someone registered `endpulse` previously but the repo is gone. Contact GitHub Support to reclaim, or rename the action in `action.yml` to `endpulse-health-check`.
- **"Icon not valid"** — `action.yml` must use an exact Feather icon name. Typos silently fail.
- **"Description too long"** — trim to 125 chars. Tagline form: "Multi-endpoint API health CLI with assertions, SSL, and CI exit codes."
