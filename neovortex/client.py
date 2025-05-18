from typing import Dict, Optional, Any, Union, List
import httpx
import logging
import time
from .request import NeoVortexRequest
from .response import NeoVortexResponse
from .middleware import MiddlewareManager
from .exceptions import NeoVortexError
from .hooks import HookManager
from .auth.base import AuthBase
from .utils.rate_limiter import RateLimiter
from .plugins import registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NeoVortexClient:
    """Synchronous HTTP client for NeoVortex with advanced features."""
    
    def __init__(
        self,
        base_url: str = "",
        timeout: float = 30.0,
        auth: Optional[AuthBase] = None,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True,
        max_retries: int = 3,
        max_connections: int = 100,
        max_keepalive: int = 20,
    ):
        self.base_url = base_url
        self.proxies = proxies
        if proxies:
            for key, value in proxies.items():
                if value and not value.startswith("https://"):
                    raise NeoVortexError(f"Non-HTTPS proxy detected for {key}. Use HTTPS instead.")
        self.client = httpx.Client(
            timeout=timeout,
            verify=verify_ssl,
            http2=True,
            limits=httpx.Limits(
                max_connections=max_connections,
                max_keepalive_connections=max_keepalive,
            ),
            mounts={
                "https://": httpx.HTTPTransport(proxy=proxies.get("https")) if proxies else None,
            } if proxies else None,
        )
        self.auth = auth
        self.headers = headers or {}
        self.middleware = MiddlewareManager()
        self.hooks = HookManager()
        self.rate_limiter = RateLimiter()
        self.max_retries = max_retries

    def enable_plugin(self, plugin_name: str):
        registry.enable(plugin_name)

    def disable_plugin(self, plugin_name: str):
        registry.disable(plugin_name)

    def _handle_auth(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Handle authentication for the request."""
        if self.auth:
            request = self.auth.apply(request)
        return request

    def _process_plugins(self, request: NeoVortexRequest, response: Optional[NeoVortexResponse] = None, start_time: Optional[float] = None) -> Union[NeoVortexRequest, NeoVortexResponse]:
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

    def request(
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
        """Send an HTTP request with middleware and hooks."""
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
            request = self._handle_auth(request)
            self.hooks.run("pre_request", request)
            request = self.middleware.process_request(request)
            start_time = time.time()
            request = self._process_plugins(request)
            self.rate_limiter.check_limit(request)

            response = self._send_request(request)
            response = self.middleware.process_response(response)
            response = self._process_plugins(request, response, start_time)
            self.hooks.run("post_response", response)
            self.rate_limiter.update_from_response(response)
            return response
        except Exception as e:
            if sentry_plugin := registry.get("sentry"):
                sentry_plugin.capture_exception(e)
            raise NeoVortexError(f"Request failed: {str(e)}") from e

    def _build_url(self, url: str) -> str:
        return f"{self.base_url}{url}" if self.base_url else url

    def _send_request(self, request: NeoVortexRequest) -> NeoVortexResponse:
        if metrics_plugin := registry.get("metrics"):
            metrics_plugin.track_start()
        for attempt in range(self.max_retries):
            try:
                httpx_response = self.client.request(
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
                logger.warning(f"Retrying request: {str(e)}")

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()