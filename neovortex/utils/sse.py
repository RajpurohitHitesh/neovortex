import aiohttp
from typing import AsyncGenerator
from ..exceptions import NeoVortexError

class SSEHandler:
    """Handles Server-Sent Events."""
    
    def __init__(self, url: str):
        self.url = url

    async def stream(self) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status != 200:
                    raise NeoVortexError(f"SSE connection failed: {response.status}")
                async for line in response.content:
                    if line:
                        yield line.decode("utf-8")