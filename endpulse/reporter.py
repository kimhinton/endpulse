from __future__ import annotations

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
    results: list[EndpointResult], title: str = "Endpoint Health Report"
) -> Table:
    table = Table(title=title, show_lines=True)

    table.add_column("URL", style="cyan", no_wrap=True, max_width=60)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Code", justify="center", width=6)
    table.add_column("Time (ms)", justify="right", width=12)
    table.add_column("Size", justify="right", width=10)
    table.add_column("Info", style="dim", max_width=40)

    for r in results:
        info = ""
        if r.error:
            info = r.error
        elif r.failed_assertions:
            info = "FAIL: " + ", ".join(r.failed_assertions)

        table.add_row(
            r.url,
            STATUS_STYLE.get(r.status, str(r.status.value)),
            str(r.status_code) if r.status_code else "-",
            f"{r.response_time_ms:.1f}",
            _format_bytes(r.size_bytes) if r.size_bytes else "-",
            info,
        )

    return table


def print_table(
    results: list[EndpointResult], console: Console | None = None
) -> None:
    console = console or Console()
    console.print(build_table(results))
    _print_summary(results, console)


def print_watch_table(
    results: list[EndpointResult],
    round_num: int,
    live: Live,
) -> None:
    table = build_table(results, title=f"Watch Round {round_num}")
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
        [
            {
                "url": r.url,
                "status": r.status.value,
                "status_code": r.status_code,
                "response_time_ms": r.response_time_ms,
                "size_bytes": r.size_bytes,
                "error": r.error,
                "failed_assertions": r.failed_assertions or None,
            }
            for r in results
        ],
        indent=2,
    )


def has_failures(results: list[EndpointResult]) -> bool:
    return any(r.status in (Status.DOWN, Status.ERROR) for r in results)


def exit_with_status(results: list[EndpointResult], fail_fast: bool) -> None:
    if fail_fast and has_failures(results):
        sys.exit(1)


def _format_bytes(n: int) -> str:
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    return f"{n / (1024 * 1024):.1f}MB"
