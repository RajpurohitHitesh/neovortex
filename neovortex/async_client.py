from typing import Dict, Optional, Any, Union, List
import httpx
import asyncio
import secrets
import logging
import time
from .request import NeoVortexRequest
from .response import NeoVortexResponse
from .middleware import MiddlewareManager
from .exceptions import NeoVortexError
from .hooks import HookManager
from .auth.base import AuthBase
from .auth.oauth import OAuth2
from .utils.rate_limiter import RateLimiter
from .utils.priority_queue import PriorityQueue
from .plugins import registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncNeoVortexClient:
    """Asynchronous HTTP client for NeoVortex with advanced features."""
    
    def __init__(
        self,
        base_url: str = "",
        timeout: float = 30.0,
        auth: Optional[AuthBase] = None,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True,
        max_retries: int = 3,
        max_concurrent: int = 10,
        max_connections: int = 100,
        max_keepalive: int = 20,
    ):
        self.base_url = base_url
        self.proxies = proxies
        if proxies:
            for key, value in proxies.items():
                if value and not value.startswith("https://"):
                    raise NeoVortexError(f"Non-HTTPS proxy detected for {key}. Use HTTPS instead.")
        self.client = httpx.AsyncClient(
            timeout=timeout,
            verify=verify_ssl,
            http2=True,
            limits=httpx.Limits(
                max_connections=max_connections,
                max_keepalive_connections=max_keepalive,
            ),
            mounts={
                "https://": httpx.AsyncHTTPTransport(proxy=proxies.get("https")) if proxies else None,
            } if proxies else None,
        )
        self.auth = auth
        self.headers = headers or {}
        self.middleware = MiddlewareManager()
        self.hooks = HookManager()
        self.rate_limiter = RateLimiter()
        self.max_retries = max_retries
        self.queue = PriorityQueue(max_concurrent)

    def enable_plugin(self, plugin_name: str):
        registry.enable(plugin_name)

    def disable_plugin(self, plugin_name: str):
        registry.disable(plugin_name)

    async def _handle_auth(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Handle authentication for the request."""
        if self.auth:
            if isinstance(self.auth, OAuth2) and self.auth.expires_at < time.time() + 60:
                await self.auth.refresh()
            request = self.auth.apply(request)
        return request

    async def _process_plugins(self, request: NeoVortexRequest, response: Optional[NeoVortexResponse] = None, start_time: Optional[float] = None) -> NeoVortexResponse:
        """Process plugins for request and response."""
        for plugin_name in registry.enabled:
            plugin = registry.get(plugin_name)
            if plugin:
                if not response and hasattr(plugin, "process_request"):
                    request = plugin.process_request(request)
                elif response and hasattr(plugin, "process_response"):
                    response = plugin.process_response(request, response)
                if response and start_time and hasattr(plugin, "track_request"):
                    plugin.track_request(request, response, start_time)
        return response or request

    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        priority: int = 0,
    ) -> NeoVortexResponse:
        """Send an asynchronous HTTP request."""
        try:
            request = NeoVortexRequest(
                method=method,
                url=self._build_url(url),
                params=params,
                data=data,
                json=json,
                files=files,
                headers={**self.headers, **(headers or {})},
                priority=priority,
            )
            request = await self._handle_auth(request)
            await self.queue.put(request)
            self.hooks.run("pre_request", request)
            request = self.middleware.process_request(request)
            start_time = time.time()
            request = await self._process_plugins(request)
            await self.rate_limiter.check_limit_async(request)

            response = await self._send_request(request)
            response = self.middleware.process_response(response)
            response = await self._process_plugins(request, response, start_time)
            self.hooks.run("post_response", response)
            self.rate_limiter.update_from_response(response)
            return response
        except Exception as e:
            if sentry_plugin := registry.get("sentry"):
                sentry_plugin.capture_exception(e)
            raise NeoVortexError(f"Async request failed: {str(e)}") from e
        finally:
            await self.queue.task_done()

    async def batch_requests(
        self,
        requests: List[Dict[str, Any]],
    ) -> List[NeoVortexResponse]:
        """Send multiple requests concurrently."""
        tasks = [
            self.request(**req)
            for req in requests
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)

    def _build_url(self, url: str) -> str:
        return f"{self.base_url}{url}" if self.base_url else url

    async def _send_request(self, request: NeoVortexRequest) -> NeoVortexResponse:
        if metrics_plugin := registry.get("metrics"):
            metrics_plugin.track_start()
        for attempt in range(self.max_retries):
            try:
                httpx_response = await self.client.request(
                    method=request.method,
                    url=request.url,
                    params=request.params,
                    data=request.data,
                    json=request.json,
                    files=request.files,
                    headers=request.headers,
                )
                return NeoVortexResponse(httpx_response)
            except httpx.HTTPError as e:
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt + secrets.randbelow(100) / 1000.0)  # Exponential backoff with secure jitter

    async def close(self):
        """Close the async HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()