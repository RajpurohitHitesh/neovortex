import pytest
from neovortex.plugins.logging import LoggingPlugin
from neovortex.request import NeoVortexRequest
from neovortex.client import NeoVortexClient

def test_logging_plugin():
    plugin = LoggingPlugin()
    with NeoVortexClient() as client:
        plugin.log_request(NeoVortexRequest("GET", "https://example.com"))
        # Verify logging output (mock logger if needed)