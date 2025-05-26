from typing import Dict, Optional, Any
from ..exceptions import NeoVortexError
from urllib.parse import urlparse

class RequestValidator:
    """Utility class for validating request parameters."""
    
    VALID_HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    MAX_URL_LENGTH = 2048  # Standard maximum URL length
    MAX_HEADER_LENGTH = 8192  # 8KB max header size
    MAX_BODY_SIZE = 100 * 1024 * 1024  # 100MB default max body size
    
    @classmethod
    def validate_method(cls, method: str) -> None:
        """Validate HTTP method."""
        if not isinstance(method, str):
            raise ValueError("Method must be a string")
        
        method_upper = method.upper()
        if method_upper not in cls.VALID_HTTP_METHODS:
            raise ValueError(f"Invalid HTTP method: {method}. Must be one of {cls.VALID_HTTP_METHODS}")
    
    @classmethod
    def validate_url(cls, url: str) -> None:
        """Validate URL."""
        if not url:
            raise ValueError("URL cannot be empty")
            
        if len(url) > cls.MAX_URL_LENGTH:
            raise ValueError(f"URL length exceeds maximum allowed length of {cls.MAX_URL_LENGTH}")
            
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid URL format")
            if parsed.scheme not in ['http', 'https']:
                raise ValueError("URL scheme must be http or https")
        except Exception as e:
            raise ValueError(f"Invalid URL: {str(e)}")
    
    @classmethod
    def validate_headers(cls, headers: Optional[Dict[str, str]]) -> None:
        """Validate request headers."""
        if headers is None:
            return
            
        if not isinstance(headers, dict):
            raise ValueError("Headers must be a dictionary")
            
        for key, value in headers.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError("Header keys and values must be strings")
            if len(key) + len(value) > cls.MAX_HEADER_LENGTH:
                raise ValueError(f"Header {key} exceeds maximum length")
    
    @classmethod
    def validate_body(cls, data: Any = None, json: Any = None) -> None:
        """Validate request body data."""
        if data is not None:
            if hasattr(data, '__len__') and len(data) > cls.MAX_BODY_SIZE:
                raise ValueError(f"Request body exceeds maximum size of {cls.MAX_BODY_SIZE} bytes")
        
        if json is not None:
            try:
                import json as json_module
                json_str = json_module.dumps(json)
                if len(json_str) > cls.MAX_BODY_SIZE:
                    raise ValueError(f"JSON body exceeds maximum size of {cls.MAX_BODY_SIZE} bytes")
            except Exception as e:
                raise ValueError(f"Invalid JSON data: {str(e)}")
    
    @classmethod
    def validate_timeout(cls, timeout: float) -> None:
        """Validate timeout value."""
        if not isinstance(timeout, (int, float)):
            raise ValueError("Timeout must be a number")
        if timeout < 0:
            raise ValueError("Timeout cannot be negative")
        if timeout > 300:  # 5 minutes max timeout
            raise ValueError("Timeout cannot exceed 300 seconds")