class NeoVortexError(Exception):
    """Base exception for NeoVortex errors."""
    pass

class RequestError(NeoVortexError):
    """Exception raised for HTTP request failures."""
    pass

class AuthError(NeoVortexError):
    """Exception raised for authentication failures."""
    pass

class RateLimitError(NeoVortexError):
    """Exception raised when rate limits are exceeded."""
    pass