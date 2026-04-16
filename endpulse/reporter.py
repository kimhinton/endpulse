from __future__ import annotations

import csv
import io
import json
import sys

from rich.console import Console
from rich.live import Live
from rich.table import Table

from endpulse.models import EndpointResult, Status

STATUS_STYLE = {
    Status.UP: "[bold green]UP[/bold green]",
    Status.DOWN: "[bold red]DOWN[/bold red]",
    Status.SLOW: "[bold yellow]SLOW[/bold yellow]",
    Status.ERROR: "[bold red]ERROR[/bold red]",
}


def build_table(
    results: list[EndpointResult],
    title: str = "Endpoint Health Report",
    *,
    show_ssl: bool = False,
) -> Table:
    table = Table(title=title, show_lines=True)

    table.add_column("URL", style="cyan", no_wrap=True, max_width=60)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Code", justify="center", width=6)
    table.add_column("Time (ms)", justify="right", width=12)
    table.add_column("Size", justify="right", width=10)
    if show_ssl:
        table.add_column("SSL Expiry", justify="right", width=14)
    table.add_column("Info", style="dim", max_width=40)

    for r in results:
        info = ""
        if r.error:
            info = r.error
        elif r.failed_assertions:
            info = "FAIL: " + ", ".join(r.failed_assertions)

        row = [
            r.url,
            STATUS_STYLE.get(r.status, str(r.status.value)),
            str(r.status_code) if r.status_code else "-",
            f"{r.response_time_ms:.1f}",
            _format_bytes(r.size_bytes) if r.size_bytes else "-",
        ]
        if show_ssl:
            row.append(_format_ssl(r))
        row.append(info)
        table.add_row(*row)

    return table


def print_table(
    results: list[EndpointResult],
    console: Console | None = None,
    *,
    show_ssl: bool = False,
) -> None:
    console = console or Console()
    console.print(build_table(results, show_ssl=show_ssl))
    _print_summary(results, console)


def print_watch_table(
    results: list[EndpointResult],
    round_num: int,
    live: Live,
    *,
    show_ssl: bool = False,
) -> None:
    table = build_table(results, title=f"Watch Round {round_num}", show_ssl=show_ssl)
    live.update(table)


def _print_summary(results: list[EndpointResult], console: Console) -> None:
    up = sum(1 for r in results if r.status == Status.UP)
    total = len(results)
    avg_ms = sum(r.response_time_ms for r in results) / total if total else 0
    failed = sum(1 for r in results if r.status in (Status.DOWN, Status.ERROR))

    console.print(
        f"\n[bold]{up}/{total}[/bold] endpoints up  |  "
        f"avg response: [bold]{avg_ms:.1f}ms[/bold]"
        + (f"  |  [bold red]{failed} failed[/bold red]" if failed else "")
    )


def to_json(results: list[EndpointResult]) -> str:
    return json.dumps(
        [_result_to_dict(r) for r in results],
        indent=2,
    )


def to_markdown(results: list[EndpointResult], *, show_ssl: bool = False) -> str:
    """Format results as a Markdown table."""
    lines: list[str] = ["## Endpoint Health Report", ""]

    headers = ["URL", "Status", "Code", "Time (ms)", "Size"]
    if show_ssl:
        headers.append("SSL Expiry")
    headers.append("Info")

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")

    for r in results:
        info = r.error or (", ".join(r.failed_assertions) if r.failed_assertions else "")
        row = [
            f"`{r.url}`",
            f"**{r.status.value}**",
            str(r.status_code) if r.status_code else "-",
            f"{r.response_time_ms:.1f}",
            _format_bytes(r.size_bytes) if r.size_bytes else "-",
        ]
        if show_ssl:
            row.append(_format_ssl(r))
        row.append(info)
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    up = sum(1 for r in results if r.status == Status.UP)
    total = len(results)
    avg_ms = sum(r.response_time_ms for r in results) / total if total else 0
    failed = sum(1 for r in results if r.status in (Status.DOWN, Status.ERROR))
    summary = f"**{up}/{total}** endpoints up | avg response: **{avg_ms:.1f}ms**"
    if failed:
        summary += f" | **{failed} failed**"
    lines.append(summary)

    return "\n".join(lines)


def to_csv(results: list[EndpointResult], *, show_ssl: bool = False) -> str:
    """Format results as CSV."""
    output = io.StringIO()
    fieldnames = [
        "url", "status", "status_code", "response_time_ms",
        "size_bytes", "error", "failed_assertions",
    ]
    if show_ssl:
        fieldnames.extend(["ssl_days_remaining", "ssl_expires"])

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for r in results:
        row: dict[str, object] = {
            "url": r.url,
            "status": r.status.value,
            "status_code": r.status_code or "",
            "response_time_ms": r.response_time_ms,
            "size_bytes": r.size_bytes,
            "error": r.error or "",
            "failed_assertions": "; ".join(r.failed_assertions) if r.failed_assertions else "",
        }
        if show_ssl and r.ssl_info:
            row["ssl_days_remaining"] = r.ssl_info.days_remaining
            row["ssl_expires"] = r.ssl_info.expires
        elif show_ssl:
            row["ssl_days_remaining"] = ""
            row["ssl_expires"] = ""
        writer.writerow(row)

    return output.getvalue()


def has_failures(results: list[EndpointResult]) -> bool:
    return any(r.status in (Status.DOWN, Status.ERROR) for r in results)


def exit_with_status(results: list[EndpointResult], fail_fast: bool) -> None:
    if fail_fast and has_failures(results):
        sys.exit(1)


def _result_to_dict(r: EndpointResult) -> dict[str, object]:
    d: dict[str, object] = {
        "url": r.url,
        "status": r.status.value,
        "status_code": r.status_code,
        "response_time_ms": r.response_time_ms,
        "size_bytes": r.size_bytes,
        "error": r.error,
        "failed_assertions": r.failed_assertions or None,
    }
    if r.ssl_info:
        d["ssl"] = {
            "issuer": r.ssl_info.issuer,
            "expires": r.ssl_info.expires,
            "days_remaining": r.ssl_info.days_remaining,
            "error": r.ssl_info.error,
        }
    return d


def _format_ssl(r: EndpointResult) -> str:
    if not r.ssl_info:
        return "-"
    if r.ssl_info.error:
        return r.ssl_info.error[:14]
    days = r.ssl_info.days_remaining
    if days < 0:
        return "EXPIRED"
    if days <= 14:
        return f"{days}d (!)"
    if days <= 30:
        return f"{days}d"
    return f"{days}d"


def _format_bytes(n: int) -> str:
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    return f"{n / (1024 * 1024):.1f}MB"
