from __future__ import annotations

import asyncio
import time
from pathlib import Path

import click
from rich.console import Console
from rich.live import Live

from endpulse import __version__
from endpulse.checker import check_endpoints
from endpulse.config import load_config, parse_cli_assertions, urls_to_configs
from endpulse.models import EndpointConfig
from endpulse.reporter import (
    exit_with_status,
    print_table,
    print_watch_table,
    to_json,
)


@click.command()
@click.argument("urls", nargs=-1)
@click.option(
    "-c", "--config", "config_path", type=click.Path(exists=True), help="YAML config file"
)
@click.option("-n", "--repeat", default=1, help="Number of rounds to run")
@click.option("-t", "--timeout", default=10.0, help="Request timeout in seconds")
@click.option("--threshold", default=1000.0, help="Slow response threshold in ms")
@click.option("--method", default="GET", help="HTTP method")
@click.option("--concurrency", default=10, help="Max concurrent requests")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option(
    "--fail", "fail_fast", is_flag=True,
    help="Exit with code 1 if any endpoint is DOWN or ERROR",
)
@click.option(
    "-a", "--assert", "assertions", multiple=True,
    help='Assertion (e.g. "body_contains:ok", "header_contains:content-type:json")',
)
@click.option(
    "-w", "--watch", "watch_interval", type=float, default=0,
    help="Watch mode: re-check every N seconds (0 = disabled)",
)
@click.version_option(version=__version__)
def main(
    urls: tuple[str, ...],
    config_path: str | None,
    repeat: int,
    timeout: float,
    threshold: float,
    method: str,
    concurrency: int,
    output_json: bool,
    fail_fast: bool,
    assertions: tuple[str, ...],
    watch_interval: float,
) -> None:
    """Check health and response times of API endpoints.

    Pass URLs as arguments or use a YAML config file.

    \b
    Examples:
      endpulse https://api.example.com/health
      endpulse https://api1.com https://api2.com --threshold 500
      endpulse -c endpoints.yaml --json
      endpulse https://api.example.com -n 5
      endpulse https://api.example.com --fail -a "body_contains:ok"
      endpulse -c endpoints.yaml -w 5

    \b
    Assertion types:
      body_contains:<text>         Response body contains text
      body_regex:<pattern>         Response body matches regex
      header_contains:<key>:<val>  Response header contains value
      status:<code>                Status code equals value
    """
    console = Console()
    parsed_assertions = parse_cli_assertions(assertions)

    if config_path:
        configs = load_config(Path(config_path))
    elif urls:
        configs = urls_to_configs(
            list(urls),
            method=method,
            timeout=timeout,
            threshold_ms=threshold,
            assertions=parsed_assertions,
        )
    else:
        console.print("[red]Error:[/red] Provide URLs or a config file (-c)")
        raise SystemExit(1)

    if watch_interval > 0:
        _run_watch(configs, concurrency, watch_interval, output_json, fail_fast, console)
    else:
        _run_once(configs, concurrency, repeat, output_json, fail_fast, console)


def _run_once(
    configs: list[EndpointConfig],
    concurrency: int,
    repeat: int,
    output_json: bool,
    fail_fast: bool,
    console: Console,
) -> None:
    all_results = []
    for round_num in range(1, repeat + 1):
        if repeat > 1:
            console.print(f"\n[bold]Round {round_num}/{repeat}[/bold]")

        results = asyncio.run(check_endpoints(configs, concurrency=concurrency))
        all_results = results

        if output_json:
            click.echo(to_json(results))
        else:
            print_table(results, console=console)

    exit_with_status(all_results, fail_fast)


def _run_watch(
    configs: list[EndpointConfig],
    concurrency: int,
    interval: float,
    output_json: bool,
    fail_fast: bool,
    console: Console,
) -> None:
    round_num = 0
    try:
        with Live(console=console, refresh_per_second=2) as live:
            while True:
                round_num += 1
                results = asyncio.run(
                    check_endpoints(configs, concurrency=concurrency)
                )

                if output_json:
                    live.stop()
                    click.echo(to_json(results))
                    live.start()
                else:
                    print_watch_table(results, round_num, live)

                if fail_fast:
                    exit_with_status(results, fail_fast)

                time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[dim]Watch stopped.[/dim]")


if __name__ == "__main__":
    main()
