from typing import Optional
import httpx

class NeoVortexError(Exception):
    """Base exception for NeoVortex."""
    def __init__(self, message: str, response: Optional[httpx.Response] = None, error_data: Optional[dict] = None):
        super().__init__(message)
        self.response = response
        self.error_data = error_data

class ValidationError(NeoVortexError):
    """Raised when request validation fails."""
    pass

class NetworkError(NeoVortexError):
    """Raised when network-related errors occur."""
    pass

class TimeoutError(NeoVortexError):
    """Raised when request times out."""
    pass

class RateLimitError(NeoVortexError):
    """Raised when rate limit is exceeded."""
    pass

class AuthenticationError(NeoVortexError):
    """Raised when authentication fails."""
    pass

class ResponseError(NeoVortexError):
    """Raised when response processing fails."""
    pass

class SecurityError(NeoVortexError):
    """Raised when security checks fail."""
    pass