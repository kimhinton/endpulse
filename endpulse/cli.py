from __future__ import annotations

import asyncio
import time
from pathlib import Path

import click
from rich.console import Console
from rich.live import Live

from endpulse import __version__
from endpulse.checker import check_endpoints
from endpulse.config import (
    generate_init_config,
    load_config,
    parse_cli_assertions,
    urls_to_configs,
)
from endpulse.models import EndpointConfig, EndpointResult
from endpulse.notifier import notify_all
from endpulse.reporter import (
    exit_with_status,
    print_table,
    print_watch_table,
    to_csv,
    to_json,
    to_markdown,
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
@click.option(
    "--json", "output_json", is_flag=True,
    help="Output as JSON (shortcut for --output json)",
)
@click.option(
    "-o", "--output", "output_format",
    type=click.Choice(["table", "json", "markdown", "csv"], case_sensitive=False),
    default="table",
    help="Output format",
)
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
@click.option("--ssl", "ssl_check", is_flag=True, help="Check SSL certificate expiry")
@click.option(
    "--notify", "notify_urls", multiple=True,
    help="Webhook URL for failure alerts (Slack, Discord, or generic)",
)
@click.option("--init", "do_init", is_flag=True, help="Generate a sample endpoints.yaml")
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
    output_format: str,
    fail_fast: bool,
    assertions: tuple[str, ...],
    watch_interval: float,
    ssl_check: bool,
    notify_urls: tuple[str, ...],
    do_init: bool,
) -> None:
    """Check health and response times of API endpoints.

    Pass URLs as arguments or use a YAML config file.

    \b
    Examples:
      endpulse https://api.example.com/health
      endpulse https://api1.com https://api2.com --threshold 500
      endpulse -c endpoints.yaml --output markdown
      endpulse https://api.example.com --ssl --fail
      endpulse -c endpoints.yaml -w 5 --notify https://hooks.slack.com/...
      endpulse --init

    \b
    Assertion types:
      body_contains:<text>         Response body contains text
      body_regex:<pattern>         Response body matches regex
      header_contains:<key>:<val>  Response header contains value
      status:<code>                Status code equals value

    \b
    Output formats:
      table      Rich terminal table (default)
      json       JSON array
      markdown   Markdown table (for CI reports)
      csv        CSV format
    """
    console = Console()

    if do_init:
        out = generate_init_config(Path.cwd())
        console.print(f"[green]Created[/green] {out}")
        return

    if output_json:
        output_format = "json"

    parsed_assertions = parse_cli_assertions(assertions)
    all_notify_urls: list[str] = list(notify_urls)

    if config_path:
        configs, config_notify = load_config(Path(config_path))
        all_notify_urls.extend(config_notify)
    elif urls:
        configs = urls_to_configs(
            list(urls),
            method=method,
            timeout=timeout,
            threshold_ms=threshold,
            assertions=parsed_assertions,
        )
    else:
        console.print("[red]Error:[/red] Provide URLs or a config file (-c), or use --init")
        raise SystemExit(1)

    if watch_interval > 0:
        _run_watch(
            configs, concurrency, watch_interval, output_format, fail_fast,
            ssl_check, all_notify_urls, console,
        )
    else:
        _run_once(
            configs, concurrency, repeat, output_format, fail_fast,
            ssl_check, all_notify_urls, console,
        )


def _output_results(
    results: list[EndpointResult],
    output_format: str,
    ssl_check: bool,
    console: Console,
) -> None:
    if output_format == "json":
        click.echo(to_json(results))
    elif output_format == "markdown":
        click.echo(to_markdown(results, show_ssl=ssl_check))
    elif output_format == "csv":
        click.echo(to_csv(results, show_ssl=ssl_check))
    else:
        print_table(results, console=console, show_ssl=ssl_check)


def _run_once(
    configs: list[EndpointConfig],
    concurrency: int,
    repeat: int,
    output_format: str,
    fail_fast: bool,
    ssl_check: bool,
    notify_urls: list[str],
    console: Console,
) -> None:
    all_results: list[EndpointResult] = []
    for round_num in range(1, repeat + 1):
        if repeat > 1:
            console.print(f"\n[bold]Round {round_num}/{repeat}[/bold]")

        results = asyncio.run(
            check_endpoints(configs, concurrency=concurrency, ssl_check=ssl_check)
        )
        all_results = results

        _output_results(results, output_format, ssl_check, console)

    if notify_urls:
        asyncio.run(notify_all(notify_urls, all_results))

    exit_with_status(all_results, fail_fast)


def _run_watch(
    configs: list[EndpointConfig],
    concurrency: int,
    interval: float,
    output_format: str,
    fail_fast: bool,
    ssl_check: bool,
    notify_urls: list[str],
    console: Console,
) -> None:
    round_num = 0
    try:
        with Live(console=console, refresh_per_second=2) as live:
            while True:
                round_num += 1
                results = asyncio.run(
                    check_endpoints(configs, concurrency=concurrency, ssl_check=ssl_check)
                )

                if output_format in ("json", "markdown", "csv"):
                    live.stop()
                    _output_results(results, output_format, ssl_check, console)
                    live.start()
                else:
                    print_watch_table(results, round_num, live, show_ssl=ssl_check)

                if notify_urls:
                    asyncio.run(notify_all(notify_urls, results))

                if fail_fast:
                    exit_with_status(results, fail_fast)

                time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[dim]Watch stopped.[/dim]")


if __name__ == "__main__":
    main()
