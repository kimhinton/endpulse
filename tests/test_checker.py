import httpx
import pytest
import respx

from endpulse.checker import check_endpoint, check_endpoints
from endpulse.models import EndpointConfig, Status


@respx.mock
@pytest.mark.asyncio
async def test_check_endpoint_up():
    respx.get("https://api.example.com/health").mock(
        return_value=httpx.Response(200, text="ok")
    )
    config = EndpointConfig(url="https://api.example.com/health")
    async with httpx.AsyncClient() as client:
        result = await check_endpoint(client, config)

    assert result.status == Status.UP
    assert result.status_code == 200
    assert result.response_time_ms > 0


@respx.mock
@pytest.mark.asyncio
async def test_check_endpoint_wrong_status():
    respx.get("https://api.example.com/health").mock(
        return_value=httpx.Response(500, text="error")
    )
    config = EndpointConfig(url="https://api.example.com/health")
    async with httpx.AsyncClient() as client:
        result = await check_endpoint(client, config)

    assert result.status == Status.ERROR
    assert result.status_code == 500


@respx.mock
@pytest.mark.asyncio
async def test_check_endpoint_timeout():
    respx.get("https://api.example.com/health").mock(
        side_effect=httpx.ReadTimeout("timeout")
    )
    config = EndpointConfig(url="https://api.example.com/health", timeout=0.1)
    async with httpx.AsyncClient() as client:
        result = await check_endpoint(client, config)

    assert result.status == Status.DOWN
    assert result.error == "Timeout"


@respx.mock
@pytest.mark.asyncio
async def test_check_endpoint_connection_error():
    respx.get("https://api.example.com/health").mock(
        side_effect=httpx.ConnectError("connection refused")
    )
    config = EndpointConfig(url="https://api.example.com/health")
    async with httpx.AsyncClient() as client:
        result = await check_endpoint(client, config)

    assert result.status == Status.DOWN
    assert "connection refused" in result.error


@respx.mock
@pytest.mark.asyncio
async def test_check_endpoints_multiple():
    respx.get("https://api1.example.com").mock(
        return_value=httpx.Response(200, text="ok")
    )
    respx.get("https://api2.example.com").mock(
        return_value=httpx.Response(200, text="ok")
    )
    configs = [
        EndpointConfig(url="https://api1.example.com"),
        EndpointConfig(url="https://api2.example.com"),
    ]
    results = await check_endpoints(configs)
    assert len(results) == 2
    assert all(r.status == Status.UP for r in results)
