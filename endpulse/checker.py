from __future__ import annotations

import asyncio
import time

import httpx

from endpulse.models import EndpointConfig, EndpointResult, Status


async def check_endpoint(
    client: httpx.AsyncClient, config: EndpointConfig
) -> EndpointResult:
    start = time.perf_counter()
    try:
        response = await client.request(
            method=config.method,
            url=config.url,
            headers=config.headers,
            timeout=config.timeout,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        body_text = response.text

        if response.status_code != config.expected_status:
            status = Status.ERROR
        elif elapsed_ms > config.threshold_ms:
            status = Status.SLOW
        else:
            status = Status.UP

        result = EndpointResult(
            url=config.url,
            status_code=response.status_code,
            response_time_ms=round(elapsed_ms, 2),
            status=status,
            headers={k.lower(): v for k, v in response.headers.items()},
            size_bytes=len(response.content),
            body=body_text,
        )

        for assertion in config.assertions:
            if not assertion.check(result):
                result.failed_assertions.append(assertion.describe())
                result.status = Status.ERROR

        return result
    except httpx.TimeoutException:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return EndpointResult(
            url=config.url,
            response_time_ms=round(elapsed_ms, 2),
            status=Status.DOWN,
            error="Timeout",
        )
    except httpx.RequestError as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return EndpointResult(
            url=config.url,
            response_time_ms=round(elapsed_ms, 2),
            status=Status.DOWN,
            error=str(e),
        )


async def check_endpoints(
    configs: list[EndpointConfig],
    concurrency: int = 10,
) -> list[EndpointResult]:
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_check(
        client: httpx.AsyncClient, config: EndpointConfig
    ) -> EndpointResult:
        async with semaphore:
            return await check_endpoint(client, config)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [bounded_check(client, cfg) for cfg in configs]
        return await asyncio.gather(*tasks)
