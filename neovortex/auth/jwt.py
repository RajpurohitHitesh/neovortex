from typing import Dict, Optional
from .base import AuthBase
from ..request import NeoVortexRequest
from ..exceptions import AuthError
import jwt
import time

class JWTAuth(AuthBase):
    """JWT authentication handler with generation and validation."""
    
    def __init__(
        self,
        secret: Optional[str] = None,
        token: Optional[str] = None,
        algorithm: str = "HS256",
        payload: Optional[Dict] = None,
    ):
        self.secret = secret
        self.token = token
        self.algorithm = algorithm
        self.payload = payload or {}

    def generate_token(self, expires_in: int = 3600) -> str:
        """Generate a new JWT token."""
        if not self.secret:
            raise AuthError("Secret key required for token generation")
        payload = {
            **self.payload,
            "exp": int(time.time()) + expires_in,
            "iat": int(time.time()),
        }
        self.token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return self.token

    def validate_token(self, token: str) -> Dict:
        """Validate a JWT token."""
        if not self.secret:
            raise AuthError("Secret key required for token validation")
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.PyJWTError as e:
            raise AuthError(f"JWT validation failed: {str(e)}") from e

    def apply(self, request: NeoVortexRequest) -> NeoVortexRequest:
        if not self.token:
            self.generate_token()
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request