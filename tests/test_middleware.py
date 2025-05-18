import pytest
from neovortex.middleware import MiddlewareManager
from neovortex.request import NeoVortexRequest

def test_middleware_request():
    manager = MiddlewareManager()
    def middleware(req: NeoVortexRequest) -> NeoVortexRequest:
        req.headers["X-Test"] = "test"
        return req
    manager.add_request_middleware(middleware)
    request = NeoVortexRequest("GET", "https://example.com")
    processed = manager.process_request(request)
    assert processed.headers["X-Test"] == "test"