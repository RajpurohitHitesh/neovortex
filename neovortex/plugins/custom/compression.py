from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse
import gzip
import zlib

class CompressionPlugin:
    """Handles request/response compression (gzip, deflate)."""
    
    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        if request.data and isinstance(request.data, bytes):
            request.headers["Content-Encoding"] = "gzip"
            request.data = gzip.compress(request.data)
        return request

    def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse:
        encoding = response.headers.get("Content-Encoding")
        if encoding == "gzip" and response.content:
            response.content = gzip.decompress(response.content)
            response.text = response.content.decode("utf-8")
            del response.headers["Content-Encoding"]
        elif encoding == "deflate" and response.content:
            response.content = zlib.decompress(response.content)
            response.text = response.content.decode("utf-8")
            del response.headers["Content-Encoding"]
        return response