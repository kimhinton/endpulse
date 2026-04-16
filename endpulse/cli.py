from __future__ import annotations

import asyncio
from pathlib import Path

import click
from rich.console import Console

from endpulse import __version__
from endpulse.checker import check_endpoints
from endpulse.config import load_config, urls_to_configs
from endpulse.reporter import print_table, to_json


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
) -> None:
    """Check health and response times of API endpoints.

    Pass URLs as arguments or use a YAML config file.

    \b
    Examples:
      endpulse https://api.example.com/health
      endpulse https://api1.com https://api2.com --threshold 500
      endpulse -c endpoints.yaml --json
      endpulse https://api.example.com -n 5
    """
    console = Console()

    if config_path:
        configs = load_config(Path(config_path))
    elif urls:
        configs = urls_to_configs(
            list(urls), method=method, timeout=timeout, threshold_ms=threshold
        )
    else:
        console.print("[red]Error:[/red] Provide URLs or a config file (-c)")
        raise SystemExit(1)

    for round_num in range(1, repeat + 1):
        if repeat > 1:
            console.print(f"\n[bold]Round {round_num}/{repeat}[/bold]")

        results = asyncio.run(check_endpoints(configs, concurrency=concurrency))

        if output_json:
            click.echo(to_json(results))
        else:
            print_table(results, console=console)


if __name__ == "__main__":
    main()
