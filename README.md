# NeoVortex

[![PyPI](https://img.shields.io/pypi/v/neovortex?color=%231182C2&label=PyPI)](https://pypi.org/project/neovortex/)
[![Python](https://img.shields.io/badge/Python->3.9-%23FFD140)](https://www.python.org/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/neovortex?label=Installs)](https://pypi.org/project/neovortex/)
![Static Badge](https://img.shields.io/badge/License-MIT-blue)
[![CI](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/ci.yml/badge.svg)](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/ci.yml)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=RajpurohitHitesh_neovortex&metric=bugs)](https://sonarcloud.io/summary/new_code?id=RajpurohitHitesh_neovortex)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=RajpurohitHitesh_neovortex&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=RajpurohitHitesh_neovortex)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=RajpurohitHitesh_neovortex&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=RajpurohitHitesh_neovortex)
[![Python application](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-app.yml/badge.svg)](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-app.yml)
[![Python Package using Conda](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-package-conda.yml)
[![Python package](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-package.yml/badge.svg)](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-package.yml)
[![Publish to PyPI](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-publish.yml/badge.svg)](https://github.com/RajpurohitHitesh/neovortex/actions/workflows/python-publish.yml)

**NeoVortex** is a modern, high-performance HTTP client library for Python 3.9+, designed to simplify and enhance interactions with APIs. Built with a focus on flexibility, extensibility, and developer experience, it provides a robust set of features for both synchronous and asynchronous HTTP requests, advanced authentication, middleware, plugins, and more. Whether you're a beginner or an experienced developer, NeoVortex makes API interactions intuitive and powerful.

This README provides a detailed guide to using NeoVortex, covering every feature, plugin, and how to extend the library with custom plugins. It also includes examples and step-by-step instructions to help new coders understand and contribute to the project.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Features](#core-features)
   - [HTTP Methods and Simple API](#http-methods-and-simple-api)
   - [Synchronous and Asynchronous Requests](#synchronous-and-asynchronous-requests)
   - [Streaming for Large Data](#streaming-for-large-data)
   - [Error Handling](#error-handling)
   - [Content Type Support](#content-type-support)
4. [Enhanced Asynchronous Capabilities](#enhanced-asynchronous-capabilities)
   - [Concurrent Request Pools](#concurrent-request-pools)
   - [Asyncio Integration](#asyncio-integration)
   - [Retry Logic](#retry-logic)
5. [Modern Protocol Support](#modern-protocol-support)
   - [HTTP/2 and HTTP/3](#http2-and-http3)
   - [WebSocket Support](#websocket-support)
6. [Advanced Authentication](#advanced-authentication)
   - [OAuth 1.0a](#oauth-1.0a)
   - [OAuth 2.0](#oauth-2.0)
   - [JWT Authentication](#jwt-authentication)
   - [API Key Authentication](#api-key-authentication)
7. [Middleware and Extensibility](#middleware-and-extensibility)
   - [Middleware System](#middleware-system)
   - [Plugin Architecture](#plugin-architecture)
8. [Performance Optimization](#performance-optimization)
   - [High-Performance Libraries](#high-performance-libraries)
   - [Connection Pooling](#connection-pooling)
9. [Testing and Mocking](#testing-and-mocking)
10. [Proxy and Security](#proxy-and-security)
    - [Proxy Support](#proxy-support)
    - [SSL/TLS Verification](#ssl-tls-verification)
11. [Developer Experience](#developer-experience)
    - [Type Hints](#type-hints)
    - [Documentation](#documentation)
    - [CLI Tool](#cli-tool)
12. [Unique Features](#unique-features)
    - [Rate Limit Awareness](#rate-limit-awareness)
    - [Response Caching](#response-caching)
    - [Request Validation](#request-validation)
    - [Event Hooks](#event-hooks)
    - [Metrics and Monitoring](#metrics-and-monitoring)
13. [Request Batching and Aggregation](#request-batching-and-aggregation)
14. [Dynamic Request Prioritization](#dynamic-request-prioritization)
15. [WebSocket and Server-Sent Events](#websocket-and-server-sent-events)
    - [WebSocket Connections](#websocket-connections)
    - [Server-Sent Events](#server-sent-events)
16. [Security Enhancements](#security-enhancements)
    - [Vulnerability Mitigation](#vulnerability-mitigation)
    - [Payload Encryption](#payload-encryption)
    - [Secret Management](#secret-management)
17. [Offline Support](#offline-support)
18. [Plugins](#plugins)
    - [Plugin Overview](#plugin-overview)
    - [Available Plugins](#available-plugins)
    - [Creating a Custom Plugin](#creating-a-custom-plugin)
    - [Disabling a Plugin](#disabling-a-plugin)
19. [Contributing](#contributing)
20. [License](#license)

## Installation
NeoVortex requires Python 3.9 or higher. Install it using pip:

```bash
pip install neovortex
```

To install dependencies for all plugins (e.g., Redis, Sentry), use:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `httpx[http2]>=0.23.0`
- `aiohttp>=3.8.0`
- `pydantic>=1.10.0`
- `oauthlib>=3.2.0`
- `requests-oauthlib>=1.3.0`
- `pyjwt>=2.6.0`
- `redis>=4.5.0`
- `prometheus-client>=0.16.0`
- `websockets>=10.4`
- `click>=8.1.0`
- `pytest>=7.2.0`
- `cryptography>=42.0.0`
- `boto3>=1.28.0`
- `botocore>=1.31.0`
- `sentry-sdk>=1.30.0`
- `elasticsearch>=8.0.0`
- `jsonschema>=4.17.0`
- `xmltodict>=0.13.0`
- `graphql-core>=3.2.0`
- `PyYAML>=6.0.0`
- `hvac>=1.0.0`

## Quick Start
Here's a basic example to get started with NeoVortex:

```python
from neovortex import NeoVortexClient

# Synchronous request
with NeoVortexClient() as client:
    response = client.request("GET", "https://api.example.com/data")
    print(response.json_data)

# Asynchronous request
import asyncio
from neovortex import AsyncNeoVortexClient

async def main():
    async with AsyncNeoVortexClient() as client:
        response = await client.request("GET", "https://api.example.com/data")
        print(response.json_data)

asyncio.run(main())
```

This sends a GET request to an API and prints the JSON response. NeoVortex handles the request, response, and error handling automatically.

## Core Features
NeoVortex provides a robust set of core features for HTTP interactions.

### HTTP Methods and Simple API
NeoVortex supports all HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.) with a simple, intuitive API.

**Example**:
```python
with NeoVortexClient() as client:
    # GET request
    response = client.request("GET", "https://api.example.com/users")
    print(response.json_data)
    
    # POST request with JSON data
    response = client.request(
        "POST",
        "https://api.example.com/users",
        json={"name": "John", "email": "john@example.com"}
    )
    print(response.status_code)  # 201
```

The `request` method accepts parameters like `method`, `url`, `params`, `data`, `json`, `files`, and `headers`, making it easy to construct requests.

### Synchronous and Asynchronous Requests
NeoVortex supports both synchronous (`NeoVortexClient`) and asynchronous (`AsyncNeoVortexClient`) requests, allowing flexibility based on your application's needs.

**Synchronous Example**:
```python
with NeoVortexClient() as client:
    response = client.request("GET", "https://api.example.com/posts")
    print(response.text)
```

**Asynchronous Example**:
```python
import asyncio
from neovortex import AsyncNeoVortexClient

async def fetch_data():
    async with AsyncNeoVortexClient() as client:
        response = await client.request("GET", "https://api.example.com/posts")
        return response.json_data

asyncio.run(fetch_data())
```

Use `NeoVortexClient` for simple scripts or blocking operations, and `AsyncNeoVortexClient` for high-performance, concurrent tasks.

### Streaming for Large Data
NeoVortex supports streaming for large uploads and downloads, reducing memory usage.

NeoVortex supports streaming for large uploads and downloads, reducing memory usage.

**Streaming Upload Example**:
```python
with NeoVortexClient() as client:
    with open("large_file.txt", "rb") as f:
        response = client.request(
            "POST",
            "https://api.example.com/upload",
            data=f
        )
    print(response.status_code)
```

**Streaming Download Example**:
```python
with NeoVortexClient() as client:
    response = client.request("GET", "https://api.example.com/large_file")
    with open("downloaded_file.txt", "wb") as f:
        for chunk in response._response.iter_content(chunk_size=8192):
            f.write(chunk)
```

### Error Handling
NeoVortex provides comprehensive error handling with custom exceptions like `NeoVortexError`, `RequestError`, `AuthError`, and `RateLimitError`.

**Example**:
```python
from neovortex import NeoVortexClient, NeoVortexError

try:
    with NeoVortexClient() as client:
        response = client.request("GET", "https://nonexistent.example.com")
except NeoVortexError as e:
    print(f"Error: {e}")  # Error: Request failed: ...
```

### Content Type Support
NeoVortex supports JSON, multipart form-data, and custom content types.

**JSON Example**:
```python
with NeoVortexClient() as client:
    response = client.request(
        "POST",
        "https://api.example.com/data",
        json={"key": "value"}
    )
    print(response.json_data)
```

**Multipart Form-Data Example**:
```python
with NeoVortexClient() as client:
    response = client.request(
        "POST",
        "https://api.example.com/upload",
        files={"file": open("example.txt", "rb")}
    )
    print(response.status_code)
```

## Enhanced Asynchronous Capabilities
NeoVortex excels in asynchronous operations, leveraging Python's `asyncio` for high-performance API interactions.

### Concurrent Request Pools
NeoVortex supports concurrent request pools with prioritization and rate limiting.

**Example**:
```python
import asyncio
from neovortex import AsyncNeoVortexClient

async def main():
    async with AsyncNeoVortexClient(max_concurrent=5) as client:
        requests = [
            {"method": "GET", "url": "https://api.example.com/data1", "priority": 1},
            {"method": "GET", "url": "https://api.example.com/data2", "priority": 2},
        ]
        responses = await client.batch_requests(requests)
        for resp in responses:
            print(resp.json_data)

asyncio.run(main())
```

The `max_concurrent` parameter limits concurrent requests, and `priority` ensures high-priority requests are processed first.

### Asyncio Integration
NeoVortex integrates seamlessly with `asyncio` event loops, using `async/await` syntax.

**Example**:
```python
import asyncio
from neovortex import AsyncNeoVortexClient

async def fetch_multiple():
    async with AsyncNeoVortexClient() as client:
        tasks = [
            client.request("GET", f"https://api.example.com/data/{i}")
            for i in range(3)
        ]
        responses = await asyncio.gather(*tasks)
        return [resp.json_data for resp in responses]

asyncio.run(fetch_multiple())
```

### Retry Logic
NeoVortex includes built-in retry logic with exponential backoff and jitter for failed requests.

**Example**:
```python
with NeoVortexClient(max_retries=3) as client:
    response = client.request("GET", "https://unreliable-api.example.com")
    print(response.status_code)
```

If the request fails, NeoVortex retries up to `max_retries` times, with delays like 1s, 2s, 4s (plus random jitter).

## Modern Protocol Support
NeoVortex supports modern HTTP protocols and real-time communication.

### HTTP/2 and HTTP/3
NeoVortex uses `httpx` with HTTP/2 support enabled by default. HTTP/3 (QUIC) support depends on the underlying `httpx` configuration.

**Example**:
```python
with NeoVortexClient() as client:
    response = client.request("GET", "https://api.example.com")  # Uses HTTP/2 if supported
    print(response.headers)
```

### WebSocket Support
NeoVortex supports WebSocket connections for real-time APIs, with automatic reconnection logic.

**Example**:
```python
import asyncio
from neovortex.utils.websocket import WebSocketHandler

async def websocket_example():
    ws = WebSocketHandler("wss://api.example.com/ws")
    await ws.connect()
    await ws.send('{"message": "Hello"}')
    response = await ws.receive()
    print(response)

asyncio.run(websocket_example())
```

## Advanced Authentication
NeoVortex supports multiple authentication methods, making it easy to work with secure APIs.

### OAuth 1.0a
Handles OAuth 1.0a authentication for APIs like Twitter.

**Example**:
```python
from neovortex.auth.oauth import OAuth1

auth = OAuth1(
    client_key="your_client_key",
    client_secret="your_client_secret",
    resource_owner_key="your_resource_owner_key",
    resource_owner_secret="your_resource_owner_secret"
)
with NeoVortexClient(auth=auth) as client:
    response = client.request("GET", "https://api.twitter.com/1.1/statuses/home_timeline.json")
    print(response.json_data)
```

### OAuth 2.0
Supports OAuth 2.0 with automatic token refresh.

**Example**:
```python
from neovortex.auth.oauth import OAuth2

auth = OAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret",
    token_url="https://api.example.com/oauth/token",
    refresh_token="your_refresh_token"
)
async def fetch_data():
    async with AsyncNeoVortexClient(auth=auth) as client:
        response = await client.request("GET", "https://api.example.com/protected")
        print(response.json_data)

import asyncio
asyncio.run(fetch_data())
```

### JWT Authentication
Supports JSON Web Token (JWT) generation and validation.

**Example**:
```python
from neovortex.auth.jwt import JWTAuth

auth = JWTAuth(secret="your_secret", payload={"user_id": 123})
auth.generate_token(expires_in=3600)  # Generate JWT
with NeoVortexClient(auth=auth) as client:
    response = client.request("GET", "https://api.example.com/secure")
    print(response.json_data)
```

### API Key Authentication
Supports API key authentication with customizable headers.

**Example**:
```python
from neovortex.auth.api_key import APIKeyAuth

auth = APIKeyAuth(api_key="your_api_key", header_name="X-API-Key")
with NeoVortexClient(auth=auth) as client:
    response = client.request("GET", "https://api.example.com/data")
    print(response.json_data)
```

## Middleware and Extensibility
NeoVortex's middleware and plugin systems allow customization of request/response workflows.

### Middleware System
Middleware processes requests and responses using Pythonic decorators or context managers.

**Example**:
```python
from neovortex import NeoVortexClient, NeoVortexRequest

def add_header_middleware(request: NeoVortexRequest) -> NeoVortexRequest:
    request.headers["X-Custom"] = "Value"
    return request

with NeoVortexClient() as client:
    client.middleware.add_request_middleware(add_header_middleware)
    response = client.request("GET", "https://api.example.com")
    print(response.headers)
```

### Plugin Architecture
Plugins extend NeoVortex's functionality. See the [Plugins](#plugins) section for details.

## Performance Optimization
NeoVortex is optimized for performance using modern libraries and techniques.

### High-Performance Libraries
NeoVortex uses `httpx` for both synchronous and asynchronous requests, ensuring high performance with modern HTTP features like HTTP/2 support.

### Connection Pooling
NeoVortex supports connection pooling to reduce latency.

**Example**:
```python
with NeoVortexClient(max_connections=100, max_keepalive=20) as client:
    for _ in range(10):
        response = client.request("GET", "https://api.example.com")
        print(response.status_code)
```

## Testing and Mocking
NeoVortex includes built-in support for testing with pytest and unittest.

**Example**:
```python
import pytest
from neovortex import NeoVortexClient

def test_client_get():
    with NeoVortexClient() as client:
        response = client.request("GET", "https://httpbin.org/get")
        assert response.status_code == 200
```

## Proxy and Security
NeoVortex provides advanced proxy and security features.

### Proxy Support
Supports HTTP, HTTPS, and SOCKS5 proxies with rotation.

**Example**:
```python
with NeoVortexClient(proxies={"https": "http://proxy.example.com:8080"}) as client:
    response = client.request("GET", "https://api.example.com")
    print(response.json_data)
```

### SSL/TLS Verification
NeoVortex enforces SSL/TLS verification by default, with options to customize certificates.

**Example**:
```python
with NeoVortexClient(verify_ssl=False) as client:  # Disable for testing
    response = client.request("GET", "https://api.example.com")
    print(response.json_data)
```

## Developer Experience
NeoVortex prioritizes a great developer experience.

### Type Hints
Full type hint support with `mypy` compatibility.

**Example**:
```python
from neovortex import NeoVortexClient
from typing import Dict

def fetch_data(client: NeoVortexClient) -> Dict[str, Any]:
    response = client.request("GET", "https://api.example.com")
    return response.json_data
```

### Documentation
Comprehensive documentation is planned. This README serves as the primary guide.

### CLI Tool
NeoVortex includes a CLI tool for quick API testing, similar to `curl`.

**Example**:
```bash
neovortex --method GET --url https://api.example.com --headers "Authorization=Bearer token"
```

## Unique Features
NeoVortex offers unique features to enhance API interactions.

### Rate Limit Awareness
Automatically detects and respects API rate limits using headers like `X-Rate-Limit-Remaining`.

**Example**:
```python
with NeoVortexClient() as client:
    response = client.request("GET", "https://api.example.com")
    # RateLimiter updates limits based on response headers
```

### Response Caching
Supports in-memory and Redis-based caching with TTL.

**Example**:
```python
from neovortex.plugins.caching import CachePlugin

cache = CachePlugin(redis_url="redis://localhost:6379")
with NeoVortexClient() as client:
    client.enable_plugin("cache")
    response = client.request("GET", "https://api.example.com")
    cache.cache_response(response)
```

### Request Validation
Validates requests and responses using Pydantic or JSON Schema.

**Example**:
```python
from pydantic import BaseModel
from neovortex.utils.validation import RequestValidator

class UserSchema(BaseModel):
    name: str
    email: str

validator = RequestValidator(pydantic_schema=UserSchema)
with NeoVortexClient() as client:
    response = client.request("POST", "https://api.example.com", json={"name": "John", "email": "john@example.com"})
    validator.validate_response(response)
```

### Event Hooks
Customizable hooks for request/response lifecycle events.

**Example**:
```python
def log_request(request):
    print(f"Request: {request.method} {request.url}")

with NeoVortexClient() as client:
    client.hooks.register("pre_request", log_request)
    response = client.request("GET", "https://api.example.com")
```

### Metrics and Monitoring
Collects performance metrics using Prometheus.

**Example**:
```python
from neovortex.plugins.metrics import MetricsPlugin

metrics = MetricsPlugin()
with NeoVortexClient() as client:
    client.enable_plugin("metrics")
    response = client.request("GET", "https://api.example.com")
    metrics.track_request(response, start_time=time.time())
```

## Request Batching and Aggregation
NeoVortex supports batching multiple requests into a single call and aggregating responses.

**Example**:
```python
from neovortex.batch import BatchHandler
from neovortex import AsyncNeoVortexClient

async def batch_example():
    async with AsyncNeoVortexClient() as client:
        handler = BatchHandler(client)
        responses = await handler.process_batch([
            {"method": "GET", "url": "https://api.example.com/data1"},
            {"method": "GET", "url": "https://api.example.com/data2"}
        ])
        aggregated = await handler.aggregate(responses)
        print(aggregated)

asyncio.run(batch_example())
```

## Dynamic Request Prioritization
Prioritizes requests in async pools based on a `priority` parameter.

**Example**:
```python
async def prioritized_requests():
    async with AsyncNeoVortexClient() as client:
        responses = await client.batch_requests([
            {"method": "GET", "url": "https://api.example.com/urgent", "priority": 1},
            {"method": "GET", "url": "https://api.example.com/normal", "priority": 2}
        ])
        print([resp.status_code for resp in responses])

asyncio.run(prioritized_requests())
```

## WebSocket and Server-Sent Events
NeoVortex supports real-time communication.

### WebSocket Connections
Handles WebSocket connections with reconnection logic.

**Example**:
```python
from neovortex.utils.websocket import WebSocketHandler

async def ws_chat():
    ws = WebSocketHandler("wss://chat.example.com", max_reconnects=3)
    await ws.send("Hello, server!")
    response = await ws.receive()
    print(response)

asyncio.run(ws_chat())
```

### Server-Sent Events
Supports Server-Sent Events (SSE) for streaming updates.

**Example**:
```python
from neovortex.utils.sse import SSEHandler

async def sse_stream():
    sse = SSEHandler("https://api.example.com/events")
    async for event in sse.stream():
        print(event)

asyncio.run(sse_stream())
```

## Security Enhancements
NeoVortex includes advanced security features.

### Vulnerability Mitigation
Prevents SSRF and insecure redirects.

**Example**:
```python
from neovortex.utils.security import SecurityHandler

security = SecurityHandler(allowed_domains=["example.com"])
with NeoVortexClient() as client:
    security.verify_request(NeoVortexRequest("GET", "https://example.com"))
```

### Payload Encryption
Encrypts sensitive data using Fernet.

**Example**:
```python
from neovortex.utils.security import SecurityHandler

security = SecurityHandler(encryption_key=b'your_key')
encrypted = security.encrypt_payload(b"sensitive_data")
decrypted = security.decrypt_payload(encrypted)
print(decrypted)  # b"sensitive_data"
```

### Secret Management
Integrates with HashiCorp Vault for secure key storage.

**Example**:
```python
security = SecurityHandler(vault_url="http://vault:8200", vault_token="your_token")
key = security.fetch_key_from_vault("secret/path", "key_name")
```

## Offline Support
Queues requests when offline and retries when connectivity is restored.

**Example**:
```python
from neovortex.offline import OfflineHandler

offline = OfflineHandler()
with NeoVortexClient() as client:
    request = NeoVortexRequest("GET", "https://api.example.com")
    offline.queue_request(request)
    offline.retry_requests(client)
```

## Plugins
NeoVortex's plugin system allows extending functionality through modular components.

### Plugin Overview
Plugins process requests and responses, providing features like caching, logging, and monitoring. They are managed by the `PluginRegistry` class, which supports enabling/disabling plugins dynamically.

**Enabling a Plugin**:
```python
with NeoVortexClient() as client:
    client.enable_plugin("cache")
    response = client.request("GET", "https://api.example.com")
```

**Disabling a Plugin**:
```python
with NeoVortexClient() as client:
    client.disable_plugin("cache")
```

### Available Plugins
1. **[CachePlugin](PLUGINS_README.md#cacheplugin)** (`neovortex/plugins/caching.py`):
   - **Purpose**: Caches responses in Redis or in-memory with configurable TTL.
   - **Features**: Cache invalidation by URL pattern, supports Redis for persistent storage.
   - **Example**:
     ```python
     from neovortex.plugins.caching import CachePlugin

     cache = CachePlugin(redis_url="redis://localhost:6379", ttl=3600)
     with NeoVortexClient() as client:
         client.register_plugin("cache", cache)
         client.enable_plugin("cache")
         response = client.request("GET", "https://api.example.com")
         cache.cache_response(response)
         cached = cache.get_cached_response(response)
     ```

2. **[LoggingPlugin](PLUGINS_README.md#loggingplugin)** (`neovortex/plugins/logging.py`):
   - **Purpose**: Logs requests and responses to files or Elasticsearch.
   - **Features**: Configurable log levels, supports external sinks like ELK Stack.
   - **Example**:
     ```python
     from neovortex.plugins.logging import LoggingPlugin

     logger = LoggingPlugin(elasticsearch_url="http://localhost:9200")
     with NeoVortexClient() as client:
         client.register_plugin("logging", logger)
         client.enable_plugin("logging")
         response = client.request("GET", "https://api.example.com")
     ```

3. **[MetricsPlugin](PLUGINS_README.md#metricsplugin)** (`neovortex/plugins/metrics.py`):
   - **Purpose**: Exports request metrics (latency, errors) to Prometheus.
   - **Features**: Tracks per-endpoint metrics, uses singleton pattern to avoid duplicates.
   - **Example**:
     ```python
     from neovortex.plugins.metrics import MetricsPlugin

     metrics = MetricsPlugin()
     with NeoVortexClient() as client:
         client.enable_plugin("metrics")
         response = client.request("GET", "https://api.example.com")
     ```

4. **[AWS4AuthPlugin](PLUGINS_README.md#aws4authplugin)** (`neovortex/plugins/custom/aws4_auth.py`):
   - **Purpose**: Implements AWS Signature Version 4 for AWS services.
   - **Features**: Authenticates requests with AWS credentials.
   - **Example**:
     ```python
     from neovortex.plugins.custom.aws4_auth import AWS4AuthPlugin

     aws_auth = AWS4AuthPlugin(
         access_key="your_access_key",
         secret_key="your_secret_key",
         region="us-east-1",
         service="s3"
     )
     with NeoVortexClient() as client:
         client.register_plugin("aws4_auth", aws_auth)
         client.enable_plugin("aws4_auth")
         response = client.request("GET", "https://s3.amazonaws.com/bucket")
     ```

5. **[APIKeyRotationPlugin](PLUGINS_README.md#apikeyrotationplugin)** (`neovortex/plugins/custom/api_key_rotation.py`):
   - **Purpose**: Rotates API keys to avoid rate limits.
   - **Features**: Randomly selects keys from a pool.
   - **Example**:
     ```python
     from neovortex.plugins.custom.api_key_rotation import APIKeyRotationPlugin

     key_rotation = APIKeyRotationPlugin(api_keys=["key1", "key2"])
     with NeoVortexClient() as client:
         client.register_plugin("api_key_rotation", key_rotation)
         client.enable_plugin("api_key_rotation")
         response = client.request("GET", "https://api.example.com")
     ```

6. **[ETagCachePlugin](PLUGINS_README.md#etagcacheplugin)** (`neovortex/plugins/custom/etag_cache.py`):
   - **Purpose**: Caches responses using ETag headers for conditional requests.
   - **Features**: Reduces redundant requests with `If-None-Match`.
   - **Example**:
     ```python
     from neovortex.plugins.custom.etag_cache import ETagCachePlugin

     etag_cache = ETagCachePlugin(ttl=3600)
     with NeoVortexClient() as client:
         client.enable_plugin("etag_cache")
         response = client.request("GET", "https://api.example.com")
     ```

7. **[SentryPlugin](PLUGINS_README.md#sentryplugin)** (`neovortex/plugins/custom/sentry.py`):
   - **Purpose**: Integrates with Sentry for error tracking and monitoring.
   - **Features**: Captures HTTP errors and exceptions.
   - **Example**:
     ```python
     from neovortex.plugins.custom.sentry import SentryPlugin

     sentry = SentryPlugin(dsn="your_sentry_dsn")
     with NeoVortexClient() as client:
         client.register_plugin("sentry", sentry)
         client.enable_plugin("sentry")
         response = client.request("GET", "https://api.example.com")
     ```

8. **[CompressionPlugin](PLUGINS_README.md#compressionplugin)** (`neovortex/plugins/custom/compression.py`):
   - **Purpose**: Compresses request bodies and decompresses responses (gzip, deflate).
   - **Features**: Reduces bandwidth usage.
   - **Example**:
     ```python
     from neovortex.plugins.custom.compression import CompressionPlugin

     compression = CompressionPlugin()
     with NeoVortexClient() as client:
         client.enable_plugin("compression")
         response = client.request("POST", "https://api.example.com", data=b"large_data")
     ```

9. **[XMLToJSONPlugin](PLUGINS_README.md#xmltojsonplugin)** (`neovortex/plugins/custom/xml_to_json.py`):
   - **Purpose**: Converts XML responses to JSON.
   - **Features**: Simplifies handling of legacy APIs.
   - **Example**:
     ```python
     from neovortex.plugins.custom.xml_to_json import XMLToJSONPlugin

     xml_to_json = XMLToJSONPlugin()
     with NeoVortexClient() as client:
         client.enable_plugin("xml_to_json")
         response = client.request("GET", "https://api.example.com/xml")
         print(response.json_data)
     ```

10. **[DynamicThrottlePlugin](PLUGINS_README.md#dynamicthrottleplugin)** (`neovortex/plugins/custom/dynamic_throttle.py`):
    - **Purpose**: Adjusts request rates based on server feedback (latency).
    - **Features**: Adapts to API performance dynamically.
    - **Example**:
      ```python
      from neovortex.plugins.custom.dynamic_throttle import DynamicThrottlePlugin

      throttle = DynamicThrottlePlugin(initial_rps=10.0)
      with NeoVortexClient() as client:
          client.enable_plugin("dynamic_throttle")
          response = client.request("GET", "https://api.example.com")
      ```

11. **[GraphQLPlugin](PLUGINS_README.md#graphqlplugin)** (`neovortex/plugins/custom/graphql.py`):
    - **Purpose**: Simplifies GraphQL queries with schema validation and batching.
    - **Features**: Ensures valid queries and combines multiple queries.
    - **Example**:
      ```python
      from neovortex.plugins.custom.graphql import GraphQLPlugin

      graphql = GraphQLPlugin(schema_sdl="type Query { user(id: ID!): User }")
      with NeoVortexClient() as client:
          client.enable_plugin("graphql")
          response = client.request("POST", "https://api.example.com/graphql", json={"query": "{ user(id: 1) { name } }"})
      ```

12. **[CDNProxyPlugin](PLUGINS_README.md#cdnproxyplugin)** (`neovortex/plugins/custom/cdn_proxy.py`):
    - **Purpose**: Routes requests through a CDN or proxy for faster responses.
    - **Features**: Randomly selects proxies from a list.
    - **Example**:
      ```python
      from neovortex.plugins.custom.cdn_proxy import CDNProxyPlugin

      cdn_proxy = CDNProxyPlugin(proxies=["http://proxy1.example.com", "http://proxy2.example.com"])
      with NeoVortexClient() as client:
          client.register_plugin("cdn_proxy", cdn_proxy)
          client.enable_plugin("cdn_proxy")
          response = client.request("GET", "https://api.example.com")
      ```

### Creating a Custom Plugin
To create a custom plugin, follow these steps:

1. **Create the Plugin File**:
   - Place your plugin in `neovortex/plugins/custom/`.
   - Example: Create `neovortex/plugins/custom/my_plugin.py`.

   ```python
   from neovortex.request import NeoVortexRequest
   from neovortex.response import NeoVortexResponse

   class MyCustomPlugin:
       def __init__(self, config: str = "default"):
           self.config = config

       def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
           request.headers["X-My-Plugin"] = self.config
           return request

       def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse:
           response.headers["X-My-Plugin-Processed"] = "true"
           return response
   ```

2. **Update Plugin Registry**:
   - Import your plugin in `neovortex/plugins/__init__.py`.
   - Add it to `__all__`.

   ```python
   from .custom.my_plugin import MyCustomPlugin

   __all__ = [
       # Existing plugins
       "MyCustomPlugin",
       "registry",
   ]
   ```

3. **Register the Plugin**:
   - If the plugin requires specific parameters (like `api_keys` or `dsn`), register it manually in your code:

   ```python
   my_plugin = MyCustomPlugin(config="custom_value")
   with NeoVortexClient() as client:
       client.register_plugin("my_plugin", my_plugin)
       client.enable_plugin("my_plugin")
       response = client.request("GET", "https://api.example.com")
   ```

   - If no parameters are needed, add it to `_initialize_plugins` in `PluginRegistry`:

   ```python
   def _initialize_plugins(self):
       if not self._initialized:
           # Existing registrations
           self.register("my_plugin", MyCustomPlugin())
           self._initialized = True
   ```

4. **Test the Plugin**:
   - Create a test in `tests/test_plugins.py`:

   ```python
   def test_my_plugin():
       plugin = MyCustomPlugin()
       request = NeoVortexRequest("GET", "https://example.com")
       processed = plugin.process_request(request)
       assert processed.headers["X-My-Plugin"] == "default"
   ```

5. **Update Requirements**:
   - If your plugin requires new dependencies, add them to `requirements.txt`.

### Disabling a Plugin
To disable a plugin, use the `disable_plugin` method:

**Example**:
```python
with NeoVortexClient() as client:
    client.disable_plugin("cache")  # Disables caching
    response = client.request("GET", "https://api.example.com")
```

For plugins requiring parameters (e.g., `AWS4AuthPlugin`, `APIKeyRotationPlugin`, `SentryPlugin`, `CDNProxyPlugin`), they are not registered by default and must be manually enabled after registration, so they are effectively disabled unless explicitly activated.

## Contributing
We welcome contributions to NeoVortex! Follow these steps to contribute:

1. **Fork the Repository**:
   - Fork the repository on GitHub: [rajpurohithitesh/neovortex](https://github.com/rajpurohithitesh/neovortex).

2. **Clone and Set Up**:
   ```bash
   git clone https://github.com/your-username/neovortex.git
   cd neovortex
   pip install -r requirements.txt
   ```

3. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature
   ```

4. **Make Changes**:
   - Follow the coding style (use `flake8` for linting).
   - Add tests in the `tests/` directory.
   - Update documentation in `README.md` if needed.

5. **Run Tests**:
   ```bash
   pytest tests/ --verbose
   ```

6. **Lint Code**:
   ```bash
   flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
   flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
   ```

7. **Commit and Push**:
   ```bash
   git commit -m "Add your feature"
   git push origin feature/your-feature
   ```

8. **Create a Pull Request**:
   - Open a pull request on GitHub, describing your changes in detail.

9. **Code Review**:
   - Respond to feedback from maintainers (e.g., Hitesh Rajpurohit).

### Contributor Guidelines
- Ensure tests cover new features or bug fixes.
- Follow PEP 8 style guidelines.
- Keep documentation up-to-date.
- Avoid breaking changes unless discussed with maintainers.

### Contributors
- **Hitesh Rajpurohit** ([rajpurohithitesh](https://github.com/rajpurohithitesh)): Creator and lead maintainer.

Want to contribute? Start by fixing issues labeled "good first issue" or propose new plugins!

## License
NeoVortex is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**NeoVortex** is designed to be your go-to HTTP client for Python. With its rich feature set, extensible plugin system, and focus on developer experience, it simplifies API interactions while offering advanced capabilities. Dive in, explore, and contribute to make it even better!