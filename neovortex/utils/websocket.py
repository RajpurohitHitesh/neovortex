import websockets
from typing import Optional
import asyncio
from ..exceptions import NeoVortexError

class WebSocketHandler:
    """Handles WebSocket connections with automatic reconnection."""
    
    def __init__(self, url: str, max_reconnects: int = 5, reconnect_delay: float = 5.0):
        self.url = url
        self.websocket = None
        self.max_reconnects = max_reconnects
        self.reconnect_delay = reconnect_delay
        self.reconnect_attempts = 0

    async def connect(self):
        while self.reconnect_attempts < self.max_reconnects:
            try:
                self.websocket = await websockets.connect(self.url)
                self.reconnect_attempts = 0
                return
            except Exception as e:
                self.reconnect_attempts += 1
                if self.reconnect_attempts >= self.max_reconnects:
                    raise NeoVortexError(f"WebSocket connection failed after {self.max_reconnects} attempts: {str(e)}")
                await asyncio.sleep(self.reconnect_delay)

    async def send(self, message: str):
        if not self.websocket or self.websocket.closed:
            await self.connect()
        await self.websocket.send(message)

    async def receive(self) -> str:
        if not self.websocket or self.websocket.closed:
            await self.connect()
        return await self.websocket.recv()