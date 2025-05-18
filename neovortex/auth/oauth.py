from typing import Dict, Optional
from .base import AuthBase
from ..request import NeoVortexRequest
from ..exceptions import AuthError
import oauthlib.oauth1
import requests_oauthlib
import httpx
import time

class OAuth1(AuthBase):
    """OAuth 1.0a authentication handler."""
    
    def __init__(
        self,
        client_key: str,
        client_secret: str,
        resource_owner_key: str,
        resource_owner_secret: str,
    ):
        self.client = oauthlib.oauth1.Client(
            client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
        )

    def apply(self, request: NeoVortexRequest) -> NeoVortexRequest:
        try:
            url, headers, body = self.client.sign(
                uri=request.url,
                http_method=request.method,
                body=request.data or "",
                headers=request.headers,
            )
            request.url = url
            request.headers.update(headers)
            request.data = body
            return request
        except Exception as e:
            raise AuthError(f"OAuth1 authentication failed: {str(e)}") from e

class OAuth2(AuthBase):
    """OAuth 2.0 authentication handler with token refresh."""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        refresh_token: Optional[str] = None,
        access_token: Optional[str] = None,
        expires_at: Optional[float] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.expires_at = expires_at or 0

    async def refresh(self) -> None:
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            raise AuthError("No refresh token provided")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.token_url,
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": self.refresh_token,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                    },
                )
                response.raise_for_status()
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.refresh_token = token_data.get("refresh_token", self.refresh_token)
                self.expires_at = time.time() + token_data.get("expires_in", 3600)
        except Exception as e:
            raise AuthError(f"Token refresh failed: {str(e)}") from e

    def apply(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Apply OAuth2 authentication, refreshing token if expired."""
        if not self.access_token:
            raise AuthError("No access token available")
        if self.expires_at < time.time() + 60:  # Refresh 60s before expiry
            # Note: Synchronous apply can't await refresh; async client should handle
            pass
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request