from typing import Optional
from ..request import NeoVortexRequest
from ..response import NeoVortexResponse
import redis
import pickle
import time
from ..exceptions import NeoVortexError

class CachePlugin:
    """Plugin for response caching with Redis or in-memory storage."""
    
    def __init__(self, redis_url: Optional[str] = None, ttl: int = 3600):
        self.ttl = ttl
        self.redis = None
        self.memory_cache = {}
        if redis_url:
            try:
                self.redis = redis.Redis.from_url(redis_url)
            except redis.RedisError as e:
                raise NeoVortexError(f"Failed to connect to Redis: {str(e)}")

    def cache_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> None:
        cache_key = f"neovortex:{request.method}:{request.url}"
        if self.redis:
            try:
                self.redis.setex(cache_key, self.ttl, pickle.dumps(response))
            except redis.RedisError as e:
                raise NeoVortexError(f"Redis cache error: {str(e)}")
        else:
            self.memory_cache[cache_key] = (response, time.time() + self.ttl)

    def get_cached_response(self, request: NeoVortexRequest) -> Optional[NeoVortexResponse]:
        cache_key = f"neovortex:{request.method}:{request.url}"
        if self.redis:
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    return pickle.loads(cached)
            except redis.RedisError as e:
                raise NeoVortexError(f"Redis cache error: {str(e)}")
        else:
            cached, expiry = self.memory_cache.get(cache_key, (None, 0))
            if cached and time.time() < expiry:
                return cached
            if cached:
                del self.memory_cache[cache_key]
        return None

    def invalidate_cache(self, url_pattern: str) -> None:
        """Invalidate cache entries matching the URL pattern."""
        if self.redis:
            try:
                keys = self.redis.keys(f"neovortex:*:{url_pattern}")
                if keys:
                    self.redis.delete(*keys)
            except redis.RedisError as e:
                raise NeoVortexError(f"Redis cache invalidation error: {str(e)}")
        else:
            for key in list(self.memory_cache.keys()):
                if url_pattern in key:
                    del self.memory_cache[key]