"""Link checker for README and docs.

Extracts every http(s) URL from README.md, docs/*.html, docs/*.md,
docs/launch/*.md and issues a HEAD request (fallback to GET for 405).

Skips obvious placeholders (example.com, YOUR_, xxx).

Usage:
  python scripts/check_links.py
"""

from __future__ import annotations

import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

URL_RE = re.compile(r'https?://[^\s\)\"\'\>\]\<\`]+')
SKIP_SUBSTR = (
    "example.com",
    "YOUR_",
    "T00/B00",
    "xxx",
    "your/webhook",
    "123/abc",
    "hooks.slack.com/services/T00",
    "hooks.slack.com/services/YOUR",
    "127.0.0.1",
    "localhost",
)

TIMEOUT = 8


def check(url: str) -> tuple[str, int | str]:
    url = url.rstrip(".,;:!?)")
    try:
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "endpulse-link-checker/1.0"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return url, resp.status
    except urllib.error.HTTPError as e:
        if e.code in (403, 405):
            try:
                req = urllib.request.Request(
                    url,
                    method="GET",
                    headers={"User-Agent": "endpulse-link-checker/1.0"},
                )
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    return url, resp.status
            except Exception as e2:
                return url, f"{type(e2).__name__}: {e2}"
        return url, e.code
    except Exception as e:
        return url, f"{type(e).__name__}: {e}"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    files = (
        list(root.glob("*.md"))
        + list((root / "docs").glob("*.html"))
        + list((root / "docs").glob("*.md"))
        + list((root / "docs" / "launch").glob("*.md"))
    )
    urls: set[str] = set()
    for f in files:
        urls.update(URL_RE.findall(f.read_text(encoding="utf-8", errors="replace")))

    cleaned = sorted(
        u.rstrip(".,;:!?)") for u in urls
        if not any(s in u for s in SKIP_SUBSTR)
    )
    print(f"checking {len(cleaned)} URLs across {len(files)} files")

    results: list[tuple[str, int | str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for r in pool.map(check, cleaned):
            results.append(r)

    ok = [(u, s) for u, s in results if s == 200]
    warn = [(u, s) for u, s in results if isinstance(s, int) and s != 200]
    err = [(u, s) for u, s in results if not isinstance(s, int)]

    for u, s in warn:
        print(f"  [{s}] {u}")
    for u, s in err:
        print(f"  [ERR] {u}  -> {s}")

    print(f"\n{len(ok)} ok · {len(warn)} non-200 · {len(err)} errors · {len(cleaned)} total")
    return 0 if (not warn and not err) else 1


if __name__ == "__main__":
    sys.exit(main())
