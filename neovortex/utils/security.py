from typing import Dict, Optional, List
import ssl
import hashlib
from urllib.parse import urlparse
import hmac
from cryptography.fernet import Fernet
import hvac
from ..request import NeoVortexRequest
from ..response import NeoVortexResponse
from ..exceptions import NeoVortexError

class SecurityHandler:
    """Handles security-related features like SSL verification and payload encryption."""
    
    def __init__(
        self,
        verify_ssl: bool = True,
        allowed_domains: Optional[List[str]] = None,
        encryption_key: Optional[bytes] = None,
        vault_url: Optional[str] = None,
        vault_token: Optional[str] = None,
    ):
        self.verify_ssl = verify_ssl
        self.allowed_domains = allowed_domains or []
        self.fernet = Fernet(encryption_key or Fernet.generate_key()) if encryption_key else None
        self.vault_client = None
        if vault_url and vault_token:
            try:
                self.vault_client = hvac.Client(url=vault_url, token=vault_token)
            except Exception as e:
                raise NeoVortexError(f"Vault connection failed: {str(e)}")

    def fetch_key_from_vault(self, path: str, key: str) -> bytes:
        """Fetch encryption key from HashiCorp Vault."""
        if not self.vault_client:
            raise NeoVortexError("Vault client not initialized")
        try:
            secret = self.vault_client.secrets.kv.read_secret_version(path=path)
            return secret["data"]["data"][key].encode()
        except Exception as e:
            raise NeoVortexError(f"Vault key fetch failed: {str(e)}")

    def verify_request(self, request: NeoVortexRequest) -> None:
        """Verify the request for security issues like SSRF and insecure protocols."""
        parsed_url = urlparse(request.url)
        if parsed_url.scheme == "http" and not parsed_url.hostname == "localhost":
            if self.verify_ssl:
                raise NeoVortexError("Insecure HTTP URL detected. Use HTTPS or localhost.")
        if self.allowed_domains:
            if not any(parsed_url.hostname.endswith(domain) for domain in self.allowed_domains):
                raise NeoVortexError(f"Request to unauthorized domain: {parsed_url.hostname}")
        if "Location" in request.headers:
            redirect_url = urlparse(request.headers["Location"])
            if redirect_url.hostname and redirect_url.hostname not in self.allowed_domains:
                raise NeoVortexError(f"Unsafe redirect to: {redirect_url.hostname}")

    def verify_response(self, response: NeoVortexResponse) -> None:
        """Verify the response for security issues like unsafe redirects."""
        if response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get("Location")
            if location:
                parsed_url = urlparse(location)
                if parsed_url.hostname and self.allowed_domains and parsed_url.hostname not in self.allowed_domains:
                    raise NeoVortexError(f"Unsafe redirect in response to: {parsed_url.hostname}")

    def encrypt_payload(self, data: bytes) -> bytes:
        """Encrypt sensitive payload data."""
        if not self.fernet:
            raise NeoVortexError("Encryption key not provided.")
        return self.fernet.encrypt(data)

    def decrypt_payload(self, encrypted_data: bytes) -> bytes:
        """Decrypt sensitive payload data."""
        if not self.fernet:
            raise NeoVortexError("Encryption key not provided.")
        try:
            return self.fernet.decrypt(encrypted_data)
        except Exception as e:
            raise NeoVortexError(f"Decryption failed: {str(e)}")

    def sign_request(self, request: NeoVortexRequest, secret: bytes) -> NeoVortexRequest:
        """Sign the request with HMAC to ensure integrity."""
        data = f"{request.method}{request.url}".encode()
        if request.data:
            data += request.data if isinstance(request.data, bytes) else str(request.data).encode()
        signature = hmac.new(secret, data, hashlib.sha256).hexdigest()
        request.headers["X-Signature"] = signature
        return request

    def verify_signature(self, response: NeoVortexResponse, secret: bytes) -> None:
        """Verify the response signature."""
        signature = response.headers.get("X-Signature")
        if not signature:
            raise NeoVortexError("Response signature missing.")
        data = f"{response.status_code}{response.text}".encode()
        expected_signature = hmac.new(secret, data, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature.encode(), expected_signature.encode()):
            raise NeoVortexError("Response signature verification failed.")