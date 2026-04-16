from __future__ import annotations

import json

from rich.console import Console
from rich.table import Table

from endpulse.models import EndpointResult, Status

STATUS_STYLE = {
    Status.UP: "[bold green]UP[/bold green]",
    Status.DOWN: "[bold red]DOWN[/bold red]",
    Status.SLOW: "[bold yellow]SLOW[/bold yellow]",
    Status.ERROR: "[bold red]ERROR[/bold red]",
}


def print_table(results: list[EndpointResult], console: Console | None = None) -> None:
    console = console or Console()
    table = Table(title="Endpoint Health Report", show_lines=True)

    table.add_column("URL", style="cyan", no_wrap=True, max_width=60)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Code", justify="center", width=6)
    table.add_column("Time (ms)", justify="right", width=12)
    table.add_column("Size", justify="right", width=10)
    table.add_column("Error", style="dim", max_width=30)

    for r in results:
        table.add_row(
            r.url,
            STATUS_STYLE.get(r.status, str(r.status.value)),
            str(r.status_code) if r.status_code else "-",
            f"{r.response_time_ms:.1f}",
            _format_bytes(r.size_bytes) if r.size_bytes else "-",
            r.error or "",
        )

    console.print(table)

    up = sum(1 for r in results if r.status == Status.UP)
    total = len(results)
    avg_ms = sum(r.response_time_ms for r in results) / total if total else 0
    console.print(
        f"\n[bold]{up}/{total}[/bold] endpoints up  |  "
        f"avg response: [bold]{avg_ms:.1f}ms[/bold]"
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
            }
            for r in results
        ],
        indent=2,
    )


def _format_bytes(n: int) -> str:
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    return f"{n / (1024 * 1024):.1f}MB"
