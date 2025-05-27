from typing import Optional
import asyncio
import time
from ..request import NeoVortexRequest
from ..response import NeoVortexResponse
from ..exceptions import RateLimitError

class RateLimiter:
    """Handles rate limiting with token bucket algorithm and header awareness."""
    
    def __init__(self, requests_per_second: float = 10.0, bucket_size: int = 10):
        self.requests_per_second = requests_per_second
        self.bucket_size = bucket_size
        self.tokens = bucket_size
        self.last_refill = time.time()
        self.rate_limit_remaining = float('inf')
        self.rate_limit_reset = 0.0

    def _refill_tokens(self):
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.requests_per_second
        self.tokens = min(self.bucket_size, self.tokens + new_tokens)
        self.last_refill = now

    def update_from_response(self, response: NeoVortexResponse):
        """Update rate limits based on response headers."""
        try:
            remaining = response.headers.get("X-Rate-Limit-Remaining")
            reset = response.headers.get("X-Rate-Limit-Reset")
            if remaining:
                self.rate_limit_remaining = float(remaining)
            if reset:
                self.rate_limit_reset = float(reset)
        except (ValueError, TypeError):
            pass

    async def update_from_response_async(self, response: NeoVortexResponse):
        """Async version of update_from_response for async contexts."""
        self.update_from_response(response)

    def check_limit(self, request: NeoVortexRequest):
        self._refill_tokens()
        if self.rate_limit_remaining <= 0 and time.time() < self.rate_limit_reset:
            raise RateLimitError("Rate limit exceeded")
        if self.tokens < 1:
            raise RateLimitError("Token bucket empty")
        self.tokens -= 1
        self.rate_limit_remaining = max(0, self.rate_limit_remaining - 1)

    async def check_limit_async(self, request: NeoVortexRequest):
        self._refill_tokens()
        if self.rate_limit_remaining <= 0 and time.time() < self.rate_limit_reset:
            await asyncio.sleep(self.rate_limit_reset - time.time())
        if self.tokens < 1:
            await asyncio.sleep(1.0 / self.requests_per_second)
            self._refill_tokens()
        self.tokens -= 1
        self.rate_limit_remaining = max(0, self.rate_limit_remaining - 1)