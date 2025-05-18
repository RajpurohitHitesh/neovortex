from typing import Dict, Optional, Any
import httpx

class NeoVortexRequest:
    """Represents an HTTP request with NeoVortex-specific attributes."""
    
    def __init__(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        priority: int = 0,
    ):
        self.method = method.upper()
        self.url = url
        self.params = params or {}
        self.data = data
        self.json = json
        self.files = files
        self.headers = headers or {}
        self.priority = priority

    def __repr__(self):
        return f"<NeoVortexRequest {self.method} {self.url}>"