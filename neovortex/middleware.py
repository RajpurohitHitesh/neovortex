from typing import Callable, List
from .request import NeoVortexRequest
from .response import NeoVortexResponse

class MiddlewareManager:
    """Manages middleware for request and response processing."""
    
    def __init__(self):
        self.request_middleware: List[Callable[[NeoVortexRequest], NeoVortexRequest]] = []
        self.response_middleware: List[Callable[[NeoVortexResponse], NeoVortexResponse]] = []

    def add_request_middleware(self, middleware: Callable[[NeoVortexRequest], NeoVortexRequest]):
        self.request_middleware.append(middleware)

    def add_response_middleware(self, middleware: Callable[[NeoVortexResponse], NeoVortexResponse]):
        self.response_middleware.append(middleware)

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        for middleware in self.request_middleware:
            request = middleware(request)
        return request

    def process_response(self, response: NeoVortexResponse) -> NeoVortexResponse:
        for middleware in self.response_middleware:
            response = middleware(response)
        return response