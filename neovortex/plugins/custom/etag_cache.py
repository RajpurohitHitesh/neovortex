from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse
from neovortex.exceptions import NeoVortexError
import pickle
import time

class ETagCachePlugin:
    """Caches responses using ETag headers for conditional requests."""
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self.cache = {}  # {url: (response, etag, expiry)}

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        cache_key = f"{request.method}:{request.url}"
        cached = self.cache.get(cache_key)
        if cached and time.time() < cached[2]:
            request.headers["If-None-Match"] = cached[1]  # Add ETag for conditional request
        return request

    def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse:
        cache_key = f"{request.method}:{request.url}"
        etag = response.headers.get("ETag")
        if etag and response.status_code == 200:
            self.cache[cache_key] = (response, etag, time.time() + self.ttl)
        elif response.status_code == 304:  # Not Modified
            cached = self.cache.get(cache_key)
            if cached:
                return cached[0]  # Return cached response
        return response