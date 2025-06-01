from typing import Dict, Optional
from .base import AuthBase
from ..request import NeoVortexRequest

class APIKeyAuth(AuthBase):
    """API key authentication handler."""
    
    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self.api_key = api_key
        self.header_name = header_name

    def apply(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Apply API key to the request headers (legacy method)."""
        request.headers[self.header_name] = self.api_key
        return request
    
    def authenticate(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Apply API key to the request headers.
        
        This method is called by the client to authenticate the request.
        """
        return self.apply(request)