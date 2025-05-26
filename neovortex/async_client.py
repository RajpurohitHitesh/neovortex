from typing import Dict, Optional, Any, Union, List, AsyncGenerator
import httpx
import asyncio
import secrets
import logging
import time
from .request import NeoVortexRequest
from .response import NeoVortexResponse
from .middleware import MiddlewareManager
from .exceptions import (
    NeoVortexError, ValidationError, NetworkError, 
    TimeoutError, RateLimitError, ResponseError
)
from .hooks import HookManager
from .auth.base import AuthBase
from .auth.oauth import OAuth2
from .utils.rate_limiter import RateLimiter
from .utils.priority_queue import PriorityQueue
from .utils.validation import RequestValidator
from .plugins import registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncNeoVortexClient:
    """Asynchronous HTTP client for NeoVortex with advanced features."""
    
    def __init__(
        self,
        base_url: str = "",
        connect_timeout: float = 5.0,
        read_timeout: float = 30.0,
        auth: Optional[AuthBase] = None,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True,
        max_retries: int = 3,
        max_concurrent: int = 10,
        max_connections: int = 100,
        max_keepalive: int = 20,
        max_body_size: int = 100 * 1024 * 1024,  # 100MB
    ):
        """Initialize the async client with enhanced configuration options."""
        self.base_url = base_url
        self.proxies = proxies
        self.max_body_size = max_body_size
        
        # Validate timeouts
        RequestValidator.validate_timeout(connect_timeout)
        RequestValidator.validate_timeout(read_timeout)
        
        # Validate headers
        RequestValidator.validate_headers(headers)
        
        if proxies:
            for key, value in proxies.items():
                if value and not value.startswith("https://"):
                    raise SecurityError(f"Non-HTTPS proxy detected for {key}. Use HTTPS instead.")
        
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(connect=connect_timeout, read=read_timeout),
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
    
    def enable_plugin(self, plugin_name: str) -> None:
        """Enable a plugin."""
        if not isinstance(plugin_name, str):
            raise ValidationError("Plugin name must be a string")
        registry.enable(plugin_name)
    
    def disable_plugin(self, plugin_name: str) -> None:
        """Disable a plugin."""
        if not isinstance(plugin_name, str):
            raise ValidationError("Plugin name must be a string")
        registry.disable(plugin_name)
    
    async def _handle_auth(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Handle authentication for the request asynchronously."""
        if self.auth:
            try:
                if isinstance(self.auth, OAuth2):
                    request = await self.auth.apply(request)
                else:
                    request = self.auth.apply(request)
            except Exception as e:
                raise AuthenticationError(f"Authentication failed: {str(e)}")
        return request
    
    async def _process_plugins(
        self,
        request: NeoVortexRequest,
        response: Optional[NeoVortexResponse] = None,
        start_time: Optional[float] = None
    ) -> Union[NeoVortexRequest, NeoVortexResponse]:
        """Process plugins with enhanced error handling."""
        try:
            for plugin_name in registry.enabled:
                plugin = registry.get(plugin_name)
                if plugin:
                    if not response and hasattr(plugin, "process_request"):
                        request = (
                            await plugin.process_request(request)
                            if asyncio.iscoroutinefunction(plugin.process_request)
                            else plugin.process_request(request)
                        )
                    elif response and hasattr(plugin, "process_response"):
                        response = (
                            await plugin.process_response(request, response)
                            if asyncio.iscoroutinefunction(plugin.process_response)
                            else plugin.process_response(request, response)
                        )
                    if response and start_time and hasattr(plugin, "track_request"):
                        await plugin.track_request(request, response, start_time)
            return response or request
        except Exception as e:
            logger.error(f"Plugin processing error: {str(e)}")
            if sentry_plugin := registry.get("sentry"):
                await sentry_plugin.capture_exception(e)
            raise NeoVortexError(f"Plugin processing failed: {str(e)}")
    
    async def stream(
        self,
        method: str,
        url: str,
        chunk_size: int = 8192,
        **kwargs
    ) -> AsyncGenerator[bytes, None]:
        """Stream response content in chunks asynchronously."""
        try:
            async with self.client.stream(method, self._build_url(url), **kwargs) as response:
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    yield chunk
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Stream request timed out: {str(e)}")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error during streaming: {str(e)}")
    
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
        stream: bool = False,
    ) -> Union[NeoVortexResponse, AsyncGenerator[bytes, None]]:
        """Send an HTTP request with enhanced validation and error handling."""
        try:
            # Validate input parameters
            RequestValidator.validate_method(method)
            RequestValidator.validate_url(url)
            RequestValidator.validate_headers(headers)
            RequestValidator.validate_body(data, json)
            
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
            
            try:
                await self.rate_limiter.check_limit(request)
            except Exception as e:
                raise RateLimitError(str(e))
            
            if stream:
                return self.stream(method, url, **request.to_dict())
            
            response = await self._send_request(request)
            response = self.middleware.process_response(response)
            response = await self._process_plugins(request, response, start_time)
            self.hooks.run("post_response", response)
            await self.rate_limiter.update_from_response(response)
            
            return response
            
        except ValidationError:
            raise
        except TimeoutError:
            raise
        except NetworkError:
            raise
        except RateLimitError:
            raise
        except Exception as e:
            if sentry_plugin := registry.get("sentry"):
                await sentry_plugin.capture_exception(e)
            raise NeoVortexError(f"Request failed: {str(e)}")
    
    def _build_url(self, url: str) -> str:
        """Build the complete URL with validation."""
        complete_url = f"{self.base_url}{url}" if self.base_url else url
        RequestValidator.validate_url(complete_url)
        return complete_url
    
    async def _send_request(self, request: NeoVortexRequest) -> NeoVortexResponse:
        """Send the request with retry logic and enhanced error handling."""
        if metrics_plugin := registry.get("metrics"):
            metrics_plugin.track_start()
        
        last_error = None
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
                
                # Validate response
                if not isinstance(httpx_response, httpx.Response):
                    raise ResponseError("Invalid response type received from HTTP client")
                
                response = NeoVortexResponse(httpx_response)
                
                # Handle error status codes
                if response.status_code >= 400:
                    error_data = None
                    try:
                        if 'application/json' in response.headers.get('content-type', ''):
                            error_data = response.json()
                    except:
                        pass
                    
                    if response.status_code >= 500:
                        raise NetworkError(f"Server error: {response.status_code}", response=response, error_data=error_data)
                    else:
                        raise ResponseError(f"Client error: {response.status_code}", response=response, error_data=error_data)
                
                return response
                
            except httpx.TimeoutException as e:
                last_error = TimeoutError(f"Request timed out: {str(e)}")
            except httpx.NetworkError as e:
                last_error = NetworkError(f"Network error: {str(e)}")
            except (ResponseError, NetworkError) as e:
                last_error = e
            except Exception as e:
                last_error = NeoVortexError(f"Unexpected error: {str(e)}")
            
            if attempt < self.max_retries - 1:
                logger.warning(f"Retrying request (attempt {attempt + 1}/{self.max_retries}): {str(last_error)}")
                await asyncio.sleep(2 ** attempt + secrets.randbelow(100) / 1000.0)  # Exponential backoff with jitter
            else:
                raise last_error
    
    async def close(self) -> None:
        """Close the async HTTP client and cleanup resources."""
        try:
            await self.client.aclose()
        except Exception as e:
            logger.error(f"Error closing client: {str(e)}")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()