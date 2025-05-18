from typing import Any, Optional
import httpx

class NeoVortexResponse:
    """Represents an HTTP response with NeoVortex-specific attributes."""
    
    def __init__(self, httpx_response: httpx.Response):
        self._response = httpx_response
        self.status_code = httpx_response.status_code
        self.headers = dict(httpx_response.headers)
        self.content = httpx_response.content
        self.text = httpx_response.text
        self.json_data: Optional[Any] = None
        try:
            self.json_data = httpx_response.json()
        except ValueError:
            pass

    def raise_for_status(self):
        """Raise an exception for bad status codes."""
        self._response.raise_for_status()

    def __repr__(self):
        return f"<NeoVortexResponse {self.status_code}>"