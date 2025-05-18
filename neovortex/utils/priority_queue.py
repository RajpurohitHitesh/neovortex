import asyncio
from typing import Optional
from ..request import NeoVortexRequest

class PriorityQueue:
    """Priority queue for managing concurrent requests."""
    
    def __init__(self, max_concurrent: int):
        self.queue = asyncio.PriorityQueue()
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def put(self, request: NeoVortexRequest):
        await self.semaphore.acquire()
        await self.queue.put((-request.priority, request))

    async def get(self) -> NeoVortexRequest:
        _, request = await self.queue.get()
        return request

    async def task_done(self):
        self.semaphore.release()