class NeoVortexError(Exception):
    """Base exception class for all NeoVortex exceptions."""
    
    def __init__(self, message="An error occurred in NeoVortex"):
        self.message = message
        super().__init__(self.message)


class AuthError(NeoVortexError):
    """Exception raised for authentication related errors."""
    
    def __init__(self, message="Authentication error occurred"):
        self.message = message
        super().__init__(self.message)


class RequestError(NeoVortexError):
    """Exception raised for errors that occur during request preparation."""
    
    def __init__(self, message="Error occurred while preparing the request"):
        self.message = message
        super().__init__(self.message)


class ResponseError(NeoVortexError):
    """Exception raised for errors in the response handling."""
    
    def __init__(self, message="Error occurred while handling the response", 
                 status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class TimeoutError(NeoVortexError):
    """Exception raised when a request times out."""
    
    def __init__(self, message="Request timed out"):
        self.message = message
        super().__init__(self.message)


class ConnectionError(NeoVortexError):
    """Exception raised for network connection errors."""
    
    def __init__(self, message="Connection error occurred"):
        self.message = message
        super().__init__(self.message)


class ValidationError(NeoVortexError):
    """Exception raised for validation errors."""
    
    def __init__(self, message="Validation error occurred"):
        self.message = message
        super().__init__(self.message)


class PluginError(NeoVortexError):
    """Exception raised for plugin-related errors."""
    
    def __init__(self, message="Plugin error occurred"):
        self.message = message
        super().__init__(self.message)


class SSLError(NeoVortexError):
    """Exception raised for SSL/TLS-related errors."""
    
    def __init__(self, message="SSL error occurred"):
        self.message = message
        super().__init__(self.message)


class RedirectError(NeoVortexError):
    """Exception raised for redirect-related errors."""
    
    def __init__(self, message="Redirect error occurred", 
                 status_code=None, location=None):
        self.message = message
        self.status_code = status_code
        self.location = location
        super().__init__(self.message)


class RateLimitError(NeoVortexError):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, message="Rate limit exceeded", 
                 reset_time=None, limit=None, remaining=None):
        self.message = message
        self.reset_time = reset_time
        self.limit = limit
        self.remaining = remaining
        super().__init__(self.message)


class JSONDecodeError(NeoVortexError):
    """Exception raised when JSON decoding fails."""
    
    def __init__(self, message="Failed to decode JSON response"):
        self.message = message
        super().__init__(self.message)