import pytest
from neovortex.client import NeoVortexClient
from neovortex.exceptions import NeoVortexError

def test_client_get():
    with NeoVortexClient() as client:
        response = client.request("GET", "https://httpbin.org/get")
        assert response.status_code == 200
        assert response.json_data is not None

def test_client_error():
    with NeoVortexClient() as client:
        with pytest.raises(NeoVortexError):
            client.request("GET", "https://nonexistent.example.com")