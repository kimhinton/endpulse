# endpulse — FAQ

Frequently asked questions about endpulse, an async Python CLI for multi-endpoint API health checks with assertions, SSL monitoring, webhook alerts, and CI exit codes.

This FAQ complements the main README and CHANGELOG. For open-ended questions, use GitHub Discussions (see bottom of this page).

---

1. **Q: How do I install endpulse?**
   A: Run `pip install endpulse`. endpulse requires Python 3.9 or newer. For development installs with test and lint dependencies, clone the repo and run `pip install -e ".[dev]"`. The package has no mandatory system dependencies beyond CPython.

2. **Q: Which Python versions are supported?**
   A: Python 3.9, 3.10, 3.11, 3.12, and 3.13 are tested in CI. The async backend uses `asyncio` primitives available in Python 3.9+. Python 3.8 is not supported — it lacks the `asyncio.TaskGroup` patterns used internally.

3. **Q: How often is endpulse released on PyPI?**
   A: endpulse follows a release-when-ready cadence — typically every 2 to 4 weeks, more often during active feature development. Check the [CHANGELOG](../CHANGELOG.md) for dated entries. Patch releases may ship within 24 hours for critical bug fixes.

4. **Q: Why is endpulse async?**
   A: HTTP health checks are I/O-bound. Async concurrency lets a single process issue hundreds of requests in parallel without threading overhead. For a 20-endpoint check with 300 ms average latency, a synchronous tool takes 6 seconds; endpulse completes it in ~400 ms using a semaphore-bounded `aiohttp` pool.

5. **Q: When should I use endpulse versus calling `curl` directly?**
   A: Use endpulse when you need any of: multi-endpoint checks in one command, response assertions (`body_contains`, regex, header, status), exit codes for CI, watch mode, SSL expiry monitoring, webhook alerts, or structured output (JSON/Markdown/CSV). For a single one-shot request with no assertions, `curl` remains simpler.

6. **Q: Does endpulse replace Uptime Kuma or k6?**
   A: No. Uptime Kuma is a self-hosted dashboard for long-running monitoring; k6 is a load testing framework. endpulse targets the CLI/CI/cron niche — one-shot or short-duration checks with zero infrastructure. The comparison table in README shows where each tool fits.

7. **Q: How does the `--ssl` flag work?**
   A: With `--ssl`, endpulse performs a TLS handshake for each HTTPS endpoint and reads the server certificate's `notAfter` field. The SSL Expiry column shows days remaining. Certificates expiring within 14 days are flagged with `(!)`. No private key access or cert chain validation beyond the handshake is performed.

8. **Q: What is the default request timeout?**
   A: 10 seconds per request (`--timeout 10.0`). Slow responses above `--threshold` (default 1000 ms) are flagged but not failed. Use `--timeout 3` for tight CI gates or `--timeout 30` for backend health checks that occasionally run cold-start.

9. **Q: Can I run endpulse in Docker?**
   A: Yes. Any official Python 3.9+ image works: `FROM python:3.12-slim`, `RUN pip install endpulse`, `ENTRYPOINT ["endpulse"]`. No system packages are required. For Alpine, use `python:3.12-alpine` — endpulse is pure Python. A sample Dockerfile appears in the CONTRIBUTING guide.

10. **Q: How do I integrate endpulse into GitHub Actions?**
    A: Add a step: `pip install endpulse` then `endpulse -c endpoints.yaml --fail`. The `--fail` flag returns exit code 1 on any DOWN endpoint or failed assertion, which stops the workflow. For a Markdown summary, redirect `--output markdown` to `$GITHUB_STEP_SUMMARY`. Full examples are in the README CI/CD section.

11. **Q: How does endpulse compare to httpie or requests?**
    A: httpie and requests are HTTP clients — you write Python or shell scripts around them for health-check logic. endpulse is the health-check logic, packaged as a CLI: multi-endpoint orchestration, assertions, CI exit codes, and output formats are built-in. You can still pipe endpulse's JSON output to scripts for custom logic.

12. **Q: What license does endpulse use?**
    A: MIT — see [LICENSE](../LICENSE). Commercial use, modification, private use, and distribution are all permitted. Attribution (retaining the copyright notice) is the only requirement. For academic citation, see [CITATION.cff](../CITATION.cff).

13. **Q: How can I contribute?**
    A: See [CONTRIBUTING.md](../CONTRIBUTING.md). Development flow: fork → clone → `pip install -e ".[dev]"` → make changes → `pytest` → `ruff check endpulse/ tests/` → `mypy endpulse/` → open a PR. Small PRs (under 200 lines) merge faster. For feature proposals, open a Discussion or issue first.

14. **Q: What is on the roadmap?**
    A: Near-term: gRPC endpoint support, Prometheus exporter mode, HAR file output. Mid-term: TCP/UDP probe types for non-HTTP checks, DNS resolution timing breakdown, OAuth2/mTLS auth helpers. The roadmap is community-driven — feature requests on GitHub Discussions shape priorities.

15. **Q: I found a bug. Where should I report it?**
    A: Open an issue at https://github.com/kimhinton/endpulse/issues/new/choose using the "Bug report" template. Include Python version (`python --version`), endpulse version (`endpulse --version`), minimal reproduction command, and expected vs actual output. Security-sensitive reports go to [SECURITY.md](../SECURITY.md) instead.

16. **Q: How is endpulse funded, and how can I support it?**
    A: endpulse is currently maintained in personal time under MIT. GitHub Sponsors is enabled via [.github/FUNDING.yml](../.github/FUNDING.yml) — sponsorships cover maintainer time and future hosted demo costs. Alternatively, star the repo, write a tutorial, or contribute code and docs.

17. **Q: Why are webhook notifications auto-detected by URL?**
    A: endpulse recognizes Slack (`hooks.slack.com`), Discord (`discord.com/api/webhooks`), and generic endpoints by URL prefix, then formats the payload per each platform's schema. This avoids a `--notify-type` flag for common cases. For unrecognized URLs, a generic JSON payload is POSTed — consumers can parse it for custom routing.

18. **Q: Does endpulse support HTTP/2 or HTTP/3?**
    A: endpulse uses `aiohttp`, which supports HTTP/1.1 by default. HTTP/2 requires an optional backend (`aiohttp[speedups]` or a switch to `httpx` with `h2`). HTTP/3/QUIC is not currently supported; for HTTP/3 health checks, wrap `curl --http3` in a shell step until the feature lands.

---

## Discussions

For open-ended questions, feature brainstorming, or "how would I do X" scenarios, use **GitHub Discussions** at https://github.com/kimhinton/endpulse/discussions.

To enable Discussions on your fork: **Settings** → **General** → **Features** → check **Discussions**.

This FAQ aims to stay numbered and factual. Discussions handle the long-form and exploratory conversations.
