import pytest
from neovortex.auth.api_key import APIKeyAuth
from neovortex.client import NeoVortexClient

def test_api_key_auth():
    auth = APIKeyAuth("test_key")
    with NeoVortexClient(auth=auth) as client:
        response = client.request("GET", "https://httpbin.org/headers")
        assert response.json_data["headers"]["X-Api-Key"] == "test_key"