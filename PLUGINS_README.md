# NeoVortex Plugins Guide

**NeoVortex** is a powerful HTTP client library for Python 3.9+, designed with a modular plugin system to extend its functionality. Plugins allow developers to add features like caching, logging, authentication, and more, making NeoVortex highly customizable. This README focuses exclusively on the plugin system, providing an in-depth guide to all available plugins, how to create new custom plugins, enable/disable plugins, and integrate them into your projects. Whether you're a beginner or an experienced developer, this guide explains every detail with examples to ensure clarity.

This document expands on the plugin section in the main `README.md`, addressing any missed details and providing comprehensive explanations for each plugin, including their internal workings, configuration options, and practical use cases.

## Table of Contents
1. [Plugin System Overview](#plugin-system-overview)
   - [What Are Plugins?](#what-are-plugins)
   - [How Plugins Work](#how-plugins-work)
   - [Plugin Registry](#plugin-registry)
2. [Available Plugins](#available-plugins)
   - [CachePlugin](#cacheplugin)
   - [LoggingPlugin](#loggingplugin)
   - [MetricsPlugin](#metricsplugin)
   - [AWS4AuthPlugin](#aws4authplugin)
   - [APIKeyRotationPlugin](#apikeyrotationplugin)
   - [ETagCachePlugin](#etagcacheplugin)
   - [SentryPlugin](#sentryplugin)
   - [CompressionPlugin](#compressionplugin)
   - [XMLToJSONPlugin](#xmltojsonplugin)
   - [DynamicThrottlePlugin](#dynamicthrottleplugin)
   - [GraphQLPlugin](#graphqlplugin)
   - [CDNProxyPlugin](#cdnproxyplugin)
3. [Creating a Custom Plugin](#creating-a-custom-plugin)
   - [Step-by-Step Guide](#step-by-step-guide)
   - [Example Custom Plugin](#example-custom-plugin)
   - [Registering a Custom Plugin](#registering-a-custom-plugin)
   - [Testing a Custom Plugin](#testing-a-custom-plugin)
4. [Enabling and Disabling Plugins](#enabling-and-disabling-plugins)
   - [Enabling a Plugin](#enabling-a-plugin)
   - [Disabling a Plugin](#disabling-a-plugin)
   - [Plugins Requiring Manual Registration](#plugins-requiring-manual-registration)
5. [Best Practices for Plugins](#best-practices-for-plugins)
6. [Contributing to Plugins](#contributing-to-plugins)

## Plugin System Overview

### What Are Plugins?
Plugins in NeoVortex are modular components that extend the library's functionality. They allow you to customize how requests are sent and responses are processed. For example, a plugin can cache responses, log requests, or add authentication headers. Plugins are designed to be easy to use, reusable, and pluggable, enabling developers to tailor NeoVortex to specific use cases.

### How Plugins Work
Plugins are Python classes that implement methods to process requests and responses:
- **`process_request(request: NeoVortexRequest) -> NeoVortexRequest`**: Modifies the request before it's sent (e.g., adding headers).
- **`process_response(request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse`**: Modifies the response after it's received (e.g., parsing data).
- **Other methods**: Some plugins implement additional methods, like `track_request` for metrics or `cache_response` for caching.

Plugins are integrated into the request/response lifecycle in `NeoVortexClient` and `AsyncNeoVortexClient`. When a request is made, the client checks the enabled plugins and calls their `process_request` and `process_response` methods if available.

### Plugin Registry
The `PluginRegistry` class (`neovortex/plugins/__init__.py`) manages plugins, allowing you to enable, disable, or register them dynamically. It ensures plugins are initialized only when needed, preventing issues like circular imports or premature initialization.

**Example**:
```python
from neovortex import NeoVortexClient
from neovortex.plugins import registry

with NeoVortexClient() as client:
    client.enable_plugin("cache")  # Enable caching plugin
    response = client.request("GET", "https://api.example.com")
```

## Available Plugins
NeoVortex includes 12 built-in plugins, each designed for specific use cases. Below, we explain each plugin in detail, including its purpose, configuration, internal mechanics, and practical examples.

### CachePlugin
- **File**: `neovortex/plugins/caching.py`
- **Purpose**: Caches HTTP responses to reduce redundant requests, supporting both in-memory and Redis-based storage.
- **Features**:
  - Configurable TTL (time-to-live) for cached responses.
  - Redis integration for persistent caching across sessions.
  - Cache invalidation by URL pattern for fine-grained control.
  - Automatic fallback to in-memory caching if Redis is unavailable.
- **Configuration**:
  - `redis_url` (optional): URL to Redis server (e.g., `redis://localhost:6379`).
  - `ttl` (optional): Cache duration in seconds (default: 3600).
- **Mechanics**:
  - Generates a cache key using the request method and URL (`neovortex:<method>:<url>`).
  - Stores responses in Redis using `setex` for TTL or in a dictionary for in-memory caching.
  - Provides `invalidate_cache(url_pattern)` to clear cached entries matching a pattern.
- **Use Cases**:
  - Caching API responses for frequently accessed endpoints.
  - Reducing API calls in high-traffic applications.
  - Invalidating cache when API data updates.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.caching import CachePlugin

  # Initialize with Redis
  cache = CachePlugin(redis_url="redis://localhost:6379", ttl=3600)
  with NeoVortexClient() as client:
      client.register_plugin("cache", cache)
      client.enable_plugin("cache")
      # First request: Fetches from API
      response = client.request("GET", "https://api.example.com/data")
      cache.cache_response(response)
      # Second request: Returns cached response
      cached_response = cache.get_cached_response(
          NeoVortexRequest("GET", "https://api.example.com/data")
      )
      print(cached_response.json_data)

      # Invalidate cache for specific URLs
      cache.invalidate_cache("data")
  ```
- **Notes**:
  - Ensure Redis is running if using `redis_url`.
  - In-memory caching is suitable for short-lived applications.
  - Use `invalidate_cache` to refresh data when the API updates.

### LoggingPlugin
- **File**: `neovortex/plugins/logging.py`
- **Purpose**: Logs requests and responses to console, files, or external services like Elasticsearch.
- **Features**:
  - Configurable log levels (e.g., INFO, DEBUG).
  - Supports logging to Elasticsearch for distributed systems.
  - Logs detailed request/response metadata (method, URL, headers, status code).
  - Fallback to standard logging if Elasticsearch fails.
- **Configuration**:
  - `logger_name` (optional): Name of the logger (default: `neovortex`).
  - `level` (optional): Log level (default: `INFO`).
  - `elasticsearch_url` (optional): URL to Elasticsearch server (e.g., `http://localhost:9200`).
- **Mechanics**:
  - Uses Python's `logging` module for standard logging.
  - Creates log entries with timestamps, method, URL, headers, and status codes.
  - Indexes logs in Elasticsearch under `neovortex_requests` and `neovortex_responses` indices.
  - Handles Elasticsearch connection failures gracefully.
- **Use Cases**:
  - Debugging API interactions.
  - Monitoring request/response patterns in production.
  - Storing logs in ELK Stack for analysis.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.logging import LoggingPlugin

  # Initialize with Elasticsearch
  logger = LoggingPlugin(
      logger_name="neovortex_test",
      level="DEBUG",
      elasticsearch_url="http://localhost:9200"
  )
  with NeoVortexClient() as client:
      client.register_plugin("logging", logger)
      client.enable_plugin("logging")
      response = client.request("GET", "https://api.example.com")
      # Logs request and response to console and Elasticsearch
  ```
- **Notes**:
  - Ensure Elasticsearch is running if using `elasticsearch_url`.
  - Use `DEBUG` level for detailed logs during development.
  - Logs are stored in JSON format for easy parsing in external systems.

### MetricsPlugin
- **File**: `neovortex/plugins/metrics.py`
- **Purpose**: Collects and exports performance metrics (e.g., latency, error rates) to Prometheus.
- **Features**:
  - Tracks total requests, latency, errors, and active requests.
  - Supports per-endpoint and per-method metrics.
  - Uses a singleton pattern to avoid duplicate metric registrations.
  - Clears metrics between tests to prevent conflicts.
- **Configuration**: None required (singleton instance).
- **Mechanics**:
  - Uses `prometheus_client` to create `Counter`, `Histogram`, and `Gauge` metrics.
  - Metrics include:
    - `neovortex_requests_total`: Total requests by method and endpoint.
    - `neovortex_request_latency_seconds`: Request latency by method and endpoint.
    - `neovortex_errors_total`: Errors by method, endpoint, and status code.
    - `neovortex_active_requests`: Number of active requests.
  - `clear_metrics` method unregisters metrics for testing.
- **Use Cases**:
  - Monitoring API performance in production.
  - Integrating with Prometheus/Grafana for dashboards.
  - Analyzing error rates for specific endpoints.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.metrics import MetricsPlugin

  metrics = MetricsPlugin()
  with NeoVortexClient() as client:
      client.enable_plugin("metrics")
      metrics.track_start()
      response = client.request("GET", "https://api.example.com")
      metrics.track_request(
          NeoVortexRequest("GET", "https://api.example.com"),
          response,
          time.time()
      )
      # Metrics available at Prometheus endpoint
  ```
- **Notes**:
  - Requires a Prometheus server to scrape metrics.
  - Use `clear_metrics` in tests to reset the registry.
  - Metrics are labeled with method and endpoint for granularity.

### AWS4AuthPlugin
- **File**: `neovortex/plugins/custom/aws4_auth.py`
- **Purpose**: Implements AWS Signature Version 4 for authenticating requests to AWS services.
- **Features**:
  - Signs requests with AWS credentials.
  - Supports services like S3, Lambda, and DynamoDB.
  - Handles query strings, headers, and request bodies.
- **Configuration**:
  - `access_key`: AWS access key ID.
  - `secret_key`: AWS secret access key.
  - `region`: AWS region (e.g., `us-east-1`).
  - `service`: AWS service name (e.g., `s3`).
- **Mechanics**:
  - Uses `boto3` and `botocore` to generate AWS Signature V4.
  - Adds authentication headers (`Authorization`, `X-Amz-Date`, etc.) to requests.
  - Parses URL to extract path and query string for signing.
- **Use Cases**:
  - Accessing AWS APIs (e.g., S3 buckets, EC2 instances).
  - Integrating NeoVortex with AWS-based applications.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
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
      response = client.request("GET", "https://my-bucket.s3.amazonaws.com")
      print(response.json_data)
  ```
- **Notes**:
  - Requires valid AWS credentials.
  - Must be manually registered due to required parameters.
  - Ensure `boto3` and `botocore` are installed.

### APIKeyRotationPlugin
- **File**: `neovortex/plugins/custom/api_key_rotation.py`
- **Purpose**: Rotates API keys from a pool to avoid rate limits or bans.
- **Features**:
  - Randomly selects an API key for each request.
  - Configurable header name for key injection.
  - Ensures at least one key is provided.
- **Configuration**:
  - `api_keys`: List of API keys to rotate.
  - `header_name` (optional): Header to store the key (default: `X-API-Key`).
- **Mechanics**:
  - Stores the key pool and selects a random key using `random.choice`.
  - Adds the selected key to the request's headers.
  - Validates that the key list is not empty during initialization.
- **Use Cases**:
  - Bypassing rate limits on APIs with multiple keys.
  - Enhancing security by rotating keys.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.api_key_rotation import APIKeyRotationPlugin

  key_rotation = APIKeyRotationPlugin(
      api_keys=["key1", "key2", "key3"],
      header_name="Authorization"
  )
  with NeoVortexClient() as client:
      client.register_plugin("api_key_rotation", key_rotation)
      client.enable_plugin("api_key_rotation")
      response = client.request("GET", "https://api.example.com")
      print(response.headers)  # Includes rotated API key
  ```
- **Notes**:
  - Requires multiple API keys for effective rotation.
  - Must be manually registered due to required `api_keys`.
  - Ensure keys are valid for the target API.

### ETagCachePlugin
- **File**: `neovortex/plugins/custom/etag_cache.py`
- **Purpose**: Caches responses using ETag headers for conditional requests.
- **Features**:
  - Adds `If-None-Match` headers to requests based on cached ETags.
  - Returns cached responses for `304 Not Modified` status.
  - Configurable TTL for cached entries.
- **Configuration**:
  - `ttl` (optional): Cache duration in seconds (default: 3600).
- **Mechanics**:
  - Stores responses, ETags, and expiry times in an in-memory dictionary.
  - Checks for `ETag` in responses and caches them if present.
  - For `304` responses, retrieves the cached response.
- **Use Cases**:
  - Optimizing bandwidth for APIs supporting ETags.
  - Caching static or infrequently updated resources.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.etag_cache import ETagCachePlugin

  etag_cache = ETagCachePlugin(ttl=7200)
  with NeoVortexClient() as client:
      client.register_plugin("etag_cache", etag_cache)
      client.enable_plugin("etag_cache")
      # First request: Fetches and caches with ETag
      response = client.request("GET", "https://api.example.com/static")
      # Second request: Uses If-None-Match, returns cached if 304
      response = client.request("GET", "https://api.example.com/static")
      print(response.json_data)
  ```
- **Notes**:
  - Requires APIs to return `ETag` headers.
  - In-memory caching is not persistent; use `CachePlugin` for Redis.

### SentryPlugin
- **File**: `neovortex/plugins/custom/sentry.py`
- **Purpose**: Integrates with Sentry for error tracking and performance monitoring.
- **Features**:
  - Captures HTTP errors (status >= 400) and exceptions.
  - Tracks request performance with Sentry transactions.
  - Configurable environment for Sentry reporting.
- **Configuration**:
  - `dsn`: Sentry Data Source Name (required).
  - `environment` (optional): Deployment environment (default: `production`).
- **Mechanics**:
  - Initializes Sentry SDK with the provided DSN and environment.
  - Starts a transaction for each request using `sentry_sdk.start_transaction`.
  - Captures errors and exceptions with `sentry_sdk.capture_message` and `capture_exception`.
- **Use Cases**:
  - Monitoring API errors in production.
  - Tracking performance bottlenecks.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.sentry import SentryPlugin

  sentry = SentryPlugin(dsn="https://your_sentry_dsn@sentry.io/123", environment="staging")
  with NeoVortexClient() as client:
      client.register_plugin("sentry", sentry)
      client.enable_plugin("sentry")
      try:
          response = client.request("GET", "https://api.example.com/invalid")
      except Exception as e:
          sentry.capture_exception(e)
  ```
- **Notes**:
  - Requires a valid Sentry DSN.
  - Must be manually registered due to required `dsn`.
  - Ensure `sentry-sdk` is installed.

### CompressionPlugin
- **File**: `neovortex/plugins/custom/compression.py`
- **Purpose**: Compresses request bodies and decompresses responses using gzip or deflate.
- **Features**:
  - Automatically compresses request data if it's bytes.
  - Decompresses responses with `Content-Encoding: gzip` or `deflate`.
  - Updates headers to reflect compression status.
- **Configuration**: None required.
- **Mechanics**:
  - Checks if request data is bytes and applies `gzip.compress`.
  - Adds `Content-Encoding: gzip` to request headers.
  - Decompresses response content using `gzip.decompress` or `zlib.decompress`.
  - Updates response `text` and `content` attributes.
- **Use Cases**:
  - Reducing bandwidth for large request/response payloads.
  - Interacting with APIs that support compression.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.compression import CompressionPlugin

  compression = CompressionPlugin()
  with NeoVortexClient() as client:
      client.register_plugin("compression", compression)
      client.enable_plugin("compression")
      response = client.request(
          "POST",
          "https://api.example.com",
          data=b"large_data" * 1000
      )
      print(response.text)  # Decompressed response
  ```
- **Notes**:
  - Only compresses bytes data; JSON is handled separately.
  - APIs must support gzip/deflate for response decompression.

### XMLToJSONPlugin
- **File**: `neovortex/plugins/custom/xml_to_json.py`
- **Purpose**: Converts XML responses to JSON for easier processing.
- **Features**:
  - Automatically detects XML responses via `Content-Type`.
  - Converts XML to JSON using `xmltodict`.
  - Updates response `json_data`, `text`, and `content` attributes.
- **Configuration**: None required.
- **Mechanics**:
  - Checks for `xml` in `Content-Type` header.
  - Parses XML with `xmltodict.parse` and converts to JSON.
  - Sets `Content-Type` to `application/json` after conversion.
- **Use Cases**:
  - Working with legacy APIs returning XML.
  - Simplifying response parsing in JSON-based applications.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.xml_to_json import XMLToJSONPlugin

  xml_to_json = XMLToJSONPlugin()
  with NeoVortexClient() as client:
      client.register_plugin("xml_to_json", xml_to_json)
      client.enable_plugin("xml_to_json")
      response = client.request("GET", "https://api.example.com/xml_endpoint")
      print(response.json_data)  # Converted JSON
  ```
- **Notes**:
  - Requires `xmltodict` library.
  - Only processes responses with XML content type.

### DynamicThrottlePlugin
- **File**: `neovortex/plugins/custom/dynamic_throttle.py`
- **Purpose**: Dynamically adjusts request rates based on server response latency.
- **Features**:
  - Increases/decreases rate based on average latency (e.g., reduce if >1s, increase if <0.2s).
  - Configurable initial, minimum, and maximum requests per second.
  - Maintains a sliding window of recent latencies.
- **Configuration**:
  - `initial_rps` (optional): Initial requests per second (default: 10.0).
  - `min_rps` (optional): Minimum requests per second (default: 1.0).
  - `max_rps` (optional): Maximum requests per second (default: 100.0).
- **Mechanics**:
  - Tracks latencies in a list (max 10 entries).
  - Adjusts `rps` by 20% based on average latency thresholds.
  - Enforces delays using `time.sleep` for synchronous requests.
- **Use Cases**:
  - Optimizing request rates for variable API performance.
  - Preventing server overload during high-latency periods.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.dynamic_throttle import DynamicThrottlePlugin

  throttle = DynamicThrottlePlugin(initial_rps=5.0, min_rps=1.0, max_rps=50.0)
  with NeoVortexClient() as client:
      client.register_plugin("dynamic_throttle", throttle)
      client.enable_plugin("dynamic_throttle")
      for _ in range(10):
          response = client.request("GET", "https://api.example.com")
          print(response.status_code)
  ```
- **Notes**:
  - Effective for APIs with variable response times.
  - Latency thresholds (1.0s, 0.2s) can be customized if needed.

### GraphQLPlugin
- **File**: `neovortex/plugins/custom/graphql.py`
- **Purpose**: Simplifies GraphQL queries with schema validation and batching.
- **Features**:
  - Validates GraphQL queries against a schema (if provided).
  - Supports batching multiple queries into a single request.
  - Ensures syntactically correct queries using `graphql-core`.
- **Configuration**:
  - `schema_sdl` (optional): GraphQL schema in SDL format.
- **Mechanics**:
  - Parses queries with `graphql.parse` to check syntax.
  - Validates queries against the schema using `graphql.validate`.
  - Combines multiple queries into a single JSON payload for batching.
- **Use Cases**:
  - Interacting with GraphQL APIs.
  - Ensuring query correctness before sending.
  - Batching queries for efficiency.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.graphql import GraphQLPlugin

  schema = """
  type Query {
      user(id: ID!): User
  }
  type User {
      name: String
  }
  """
  graphql = GraphQLPlugin(schema_sdl=schema)
  with NeoVortexClient() as client:
      client.register_plugin("graphql", graphql)
      client.enable_plugin("graphql")
      response = client.request(
          "POST",
          "https://api.example.com/graphql",
          json={"query": "{ user(id: 1) { name } }"}
      )
      print(response.json_data)

      # Batch queries
      batch = graphql.batch_queries([
          {"query": "{ user(id: 1) { name } }"},
          {"query": "{ user(id: 2) { name } }"}
      ])
      response = client.request("POST", "https://api.example.com/graphql", json=batch)
  ```
- **Notes**:
  - Requires `graphql-core` library.
  - Schema validation is optional but recommended.

### CDNProxyPlugin
- **File**: `neovortex/plugins/custom/cdn_proxy.py`
- **Purpose**: Routes requests through a CDN or proxy for faster responses.
- **Features**:
  - Randomly selects a proxy from a provided list.
  - Adds proxy information to request headers.
  - Ensures at least one proxy is provided.
- **Configuration**:
  - `proxies`: List of proxy URLs (e.g., `["http://proxy1.com"]`).
- **Mechanics**:
  - Selects a random proxy using `random.choice`.
  - Adds `X-Proxy` header with the selected proxy URL.
  - Validates that the proxy list is not empty during initialization.
- **Use Cases**:
  - Reducing latency with CDN proxies.
  - Distributing requests across multiple proxies.
- **Example**:
  ```python
  from neovortex import NeoVortexClient
  from neovortex.plugins.custom.cdn_proxy import CDNProxyPlugin

  cdn_proxy = CDNProxyPlugin(proxies=["http://proxy1.example.com", "http://proxy2.example.com"])
  with NeoVortexClient() as client:
      client.register_plugin("cdn_proxy", cdn_proxy)
      client.enable_plugin("cdn_proxy")
      response = client.request("GET", "https://api.example.com")
      print(response.headers["X-Proxy"])  # Random proxy URL
  ```
- **Notes**:
  - Requires valid proxy URLs.
  - Must be manually registered due to required `proxies`.

## Creating a Custom Plugin
Custom plugins allow you to extend NeoVortex with new functionality. Here's a detailed guide to creating, registering, and testing a custom plugin.

### Step-by-Step Guide
1. **Create the Plugin File**:
   - Place your plugin in `neovortex/plugins/custom/`.
   - The plugin should be a Python class with optional `process_request` and `process_response` methods.
   - Example file: `neovortex/plugins/custom/custom_header.py`.

2. **Implement the Plugin**:
   - Define `__init__` for configuration (if needed).
   - Implement `process_request` to modify requests and `process_response` to modify responses.
   - Use `NeoVortexRequest` and `NeoVortexResponse` types for type safety.

3. **Update Plugin Registry**:
   - Import the plugin in `neovortex/plugins/__init__.py`.
   - Add it to `__all__`.

4. **Register the Plugin**:
   - If the plugin requires parameters, register it manually in your code.
   - If no parameters are needed, add it to `PluginRegistry._initialize_plugins`.

5. **Test the Plugin**:
   - Create tests in `tests/test_plugins.py` to verify functionality.
   - Use pytest to run tests.

6. **Update Dependencies**:
   - Add any new dependencies to `requirements.txt`.

### Example Custom Plugin
Let's create a plugin that adds a custom header to requests and logs response sizes.

**File**: `neovortex/plugins/custom/custom_header.py`
```python
from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse

class CustomHeaderPlugin:
    """Adds a custom header to requests and logs response size."""
    def __init__(self, header_name: str, header_value: str):
        self.header_name = header_name
        self.header_value = header_value

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        request.headers[self.header_name] = self.header_value
        return request

    def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse:
        print(f"Response size: {len(response.content)} bytes")
        return response
```

**Update `neovortex/plugins/__init__.py`**:
```python
from .custom.custom_header import CustomHeaderPlugin

__all__ = [
    # Existing plugins
    "CustomHeaderPlugin",
    "registry",
]
```

**Register and Use**:
```python
from neovortex import NeoVortexClient
from neovortex.plugins.custom.custom_header import CustomHeaderPlugin

custom_header = CustomHeaderPlugin(header_name="X-Custom-Header", header_value="MyValue")
with NeoVortexClient() as client:
    client.register_plugin("custom_header", custom_header)
    client.enable_plugin("custom_header")
    response = client.request("GET", "https://api.example.com")
    # Prints response size and includes X-Custom-Header
```

### Registering a Custom Plugin
- **Manual Registration** (for plugins with parameters):
  ```python
  client.register_plugin("custom_header", CustomHeaderPlugin("X-Custom-Header", "MyValue"))
  client.enable_plugin("custom_header")
  ```
- **Automatic Registration** (for plugins without parameters):
  Update `PluginRegistry._initialize_plugins`:
  ```python
  def _initialize_plugins(self):
      if not self._initialized:
          # Existing registrations
          self.register("custom_header", CustomHeaderPlugin("X-Custom-Header", "DefaultValue"))
          self._initialized = True
  ```

### Testing a Custom Plugin
Create a test in `tests/test_plugins.py`:
```python
import pytest
from neovortex.request import NeoVortexRequest
from neovortex.plugins.custom.custom_header import CustomHeaderPlugin

def test_custom_header_plugin():
    plugin = CustomHeaderPlugin(header_name="X-Test", header_value="TestValue")
    request = NeoVortexRequest("GET", "https://example.com")
    processed = plugin.process_request(request)
    assert processed.headers["X-Test"] == "TestValue"
```

Run tests:
```bash
pytest tests/ --verbose
```

## Enabling and Disabling Plugins
NeoVortex allows you to enable or disable plugins dynamically to control which features are active.

### Enabling a Plugin
Use `enable_plugin` to activate a plugin. Plugins without required parameters (e.g., `CachePlugin`, `LoggingPlugin`) are automatically available, while others (e.g., `SentryPlugin`, `CDNProxyPlugin`) require manual registration first.

**Example**:
```python
from neovortex import NeoVortexClient
from neovortex.plugins.caching import CachePlugin

cache = CachePlugin(ttl=3600)
with NeoVortexClient() as client:
    client.register_plugin("cache", cache)
    client.enable_plugin("cache")
    response = client.request("GET", "https://api.example.com")
```

### Disabling a Plugin
Use `disable_plugin` to deactivate a plugin, preventing it from processing requests or responses.

**Example**:
```python
with NeoVortexClient() as client:
    client.enable_plugin("cache")
    client.disable_plugin("cache")  # CachePlugin no longer processes requests
    response = client.request("GET", "https://api.example.com")
```

### Plugins Requiring Manual Registration
The following plugins require manual registration due to mandatory parameters:
- `AWS4AuthPlugin`: Needs `access_key`, `secret_key`, `region`, `service`.
- `APIKeyRotationPlugin`: Needs `api_keys`.
- `SentryPlugin`: Needs `dsn`.
- `CDNProxyPlugin`: Needs `proxies`.

To use these, register them explicitly:
```python
from neovortex.plugins.custom.sentry import SentryPlugin

sentry = SentryPlugin(dsn="your_sentry_dsn")
with NeoVortexClient() as client:
    client.register_plugin("sentry", sentry)
    client.enable_plugin("sentry")
```

If not registered, these plugins are not initialized and are effectively disabled, avoiding errors during tests or runtime.

## Best Practices for Plugins
- **Minimal Dependencies**: Keep plugin dependencies lightweight to avoid bloat.
- **Error Handling**: Wrap external service calls (e.g., Redis, Elasticsearch) in try-except blocks to handle failures gracefully.
- **Type Safety**: Use type hints for `NeoVortexRequest` and `NeoVortexResponse` to ensure compatibility.
- **Testing**: Write tests for both `process_request` and `process_response` methods.
- **Documentation**: Document plugin configuration and use cases clearly.
- **Conditional Registration**: For plugins with required parameters, use manual registration to prevent initialization errors.

## Contributing to Plugins
To contribute new plugins or improve existing ones:
1. Fork the repository: [rajpurohithitesh/neovortex](https://github.com/rajpurohithitesh/neovortex).
2. Create a branch: `git checkout -b feature/new-plugin`.
3. Add your plugin in `neovortex/plugins/custom/`.
4. Update `neovortex/plugins/__init__.py` and `requirements.txt` if needed.
5. Add tests in `tests/test_plugins.py`.
6. Run tests and linting:
   ```bash
   pytest tests/ --verbose
   flake8 .
   ```
7. Submit a pull request with a detailed description.

**Example Contribution**:
- Propose a new plugin for OAuth refresh token caching.
- Include tests and documentation in the pull request.
- Ensure compatibility with existing plugins.

---

This guide covers every aspect of NeoVortex's plugin system, from using built-in plugins to creating and managing custom ones. By following the examples and best practices, you can leverage NeoVortex's flexibility to build powerful API clients tailored to your needs.