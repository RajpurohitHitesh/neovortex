import time
import json
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Any, List, Union, TypeVar, Generic

import httpx

# Re-export core request and response classes
from .request import NeoVortexRequest
from .response import NeoVortexResponse

# Type variables for generic typing
T = TypeVar('T')

class HttpMethod(str, Enum):
    """HTTP methods supported by NeoVortex."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class ContentType(str, Enum):
    """Common content types used in requests and responses."""
    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"
    MULTIPART = "multipart/form-data"
    TEXT = "text/plain"
    HTML = "text/html"
    XML = "application/xml"
    BINARY = "application/octet-stream"

@dataclass
class RequestMetadata:
    """Metadata associated with a request for tracking and analytics."""
    request_id: str
    timestamp: float
    retries: int = 0
    tags: Optional[Dict[str, str]] = None
    priority: int = 0
    
    @classmethod
    def create(cls, request_id: Optional[str] = None, **kwargs) -> 'RequestMetadata':
        """Create a new request metadata object with a unique ID."""
        import uuid
        return cls(
            request_id=request_id or str(uuid.uuid4()),
            timestamp=time.time(),
            **kwargs
        )

@dataclass
class ResponseMetadata:
    """Metadata associated with a response for tracking and analytics."""
    response_time: float  # Time taken to receive response in seconds
    retries: int = 0
    cache_hit: bool = False
    size: Optional[int] = None  # Response size in bytes

class RateLimitInfo:
    """Information about rate limit from response headers."""
    
    def __init__(self, headers: Dict[str, str]):
        """Extract rate limit information from response headers."""
        self.limit = self._parse_int(headers.get("X-RateLimit-Limit"))
        self.remaining = self._parse_int(headers.get("X-RateLimit-Remaining"))
        self.reset = self._parse_float(headers.get("X-RateLimit-Reset"))
        self.retry_after = self._parse_int(headers.get("Retry-After"))
        
    @staticmethod
    def _parse_int(value: Optional[str]) -> Optional[int]:
        """Parse string to integer safely."""
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _parse_float(value: Optional[str]) -> Optional[float]:
        """Parse string to float safely."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @property
    def is_rate_limited(self) -> bool:
        """Check if the request is rate limited."""
        return self.remaining == 0 or self.retry_after is not None

class BatchRequest:
    """Container for batched requests."""
    
    def __init__(self, requests: List[NeoVortexRequest]):
        """Initialize with a list of requests."""
        self.requests = requests
        self.id = f"batch-{int(time.time())}"
        self.request_ids = [getattr(req, "id", f"req-{i}") for i, req in enumerate(requests)]

class BatchResponse:
    """Container for batched responses."""
    
    def __init__(self, responses: List[Union[NeoVortexResponse, Exception]], 
                 metadata: Optional[Dict[str, Any]] = None):
        """Initialize with a list of responses."""
        self.responses = responses
        self.metadata = metadata or {}
        self.success_count = sum(1 for r in responses if not isinstance(r, Exception))
        self.error_count = len(responses) - self.success_count

class RequestOptions:
    """Additional options for request customization."""
    
    def __init__(self, 
                 retry_strategy: Optional[str] = None,
                 cache_ttl: Optional[int] = None,
                 timeout_override: Optional[Dict[str, float]] = None,
                 follow_redirects: bool = True,
                 validate_ssl: bool = True,
                 response_type: str = 'json',
                 extra: Optional[Dict[str, Any]] = None):
        self.retry_strategy = retry_strategy
        self.cache_ttl = cache_ttl
        self.timeout_override = timeout_override
        self.follow_redirects = follow_redirects
        self.validate_ssl = validate_ssl
        self.response_type = response_type
        self.extra = extra or {}

class RequestStats:
    """Statistics about processed requests."""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.retried_requests = 0
        self.cached_responses = 0
        self.total_response_time = 0.0
    
    def record_request(self, success: bool, response_time: float, retried: bool = False, 
                       cached: bool = False) -> None:
        """Record a request in the stats."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        if retried:
            self.retried_requests += 1
        
        if cached:
            self.cached_responses += 1
        
        self.total_response_time += response_time
    
    @property
    def average_response_time(self) -> float:
        """Calculate the average response time."""
        if self.total_requests == 0:
            return 0.0
        return self.total_response_time / self.total_requests
    
    @property
    def success_rate(self) -> float:
        """Calculate the success rate as a percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100

@dataclass
class CacheEntry(Generic[T]):
    """Generic cache entry with metadata."""
    data: T
    created_at: float
    expires_at: float
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    
    @property
    def is_expired(self) -> bool:
        """Check if the cache entry is expired."""
        return time.time() > self.expires_at
    
    @property
    def age(self) -> float:
        """Get the age of the cache entry in seconds."""
        return time.time() - self.created_at

# Set of exports for better import management
__all__ = [
    'NeoVortexRequest',
    'NeoVortexResponse',
    'HttpMethod',
    'ContentType',
    'RequestMetadata',
    'ResponseMetadata',
    'RateLimitInfo',
    'BatchRequest',
    'BatchResponse',
    'RequestOptions',
    'RequestStats',
    'CacheEntry'
]