import pytest
import asyncio
from neovortex.async_client import AsyncNeoVortexClient

@pytest.mark.asyncio
async def test_async_client_get():
    async with AsyncNeoVortexClient() as client:
        response = await client.request("GET", "https://httpbin.org/get")
        assert response.status_code == 200
        assert response.json_data is not None