from typing import Optional
import httpx

class NeoVortexError(Exception):
    """Base exception for NeoVortex."""
    def __init__(self, message: str, response: Optional[httpx.Response] = None, error_data: Optional[dict] = None):
        super().__init__(message)
        self.response = response
        self.error_data = error_data

class AuthError(NeoVortexError):
    """Raised when authentication-related errors occur."""
    pass

class SecurityError(NeoVortexError):
    """Raised when a security-related error occurs."""
    pass

class AuthenticationError(NeoVortexError):
    """Raised when authentication fails."""
    pass

class ValidationError(NeoVortexError):
    """Raised when validation fails."""
    pass

class NetworkError(NeoVortexError):
    """Raised when a network error occurs."""
    pass

class TimeoutError(NeoVortexError):
    """Raised when a request times out."""
    pass

class RateLimitError(NeoVortexError):
    """Raised when rate limit is exceeded."""
    pass

class ResponseError(NeoVortexError):
    """Raised when there's an error in the response."""
    pass