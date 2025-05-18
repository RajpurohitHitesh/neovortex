from neovortex.request import NeoVortexRequest
from neovortex.exceptions import AuthError
import boto3
import botocore.auth
import botocore.credentials
from urllib.parse import urlparse
import datetime
from datetime import timezone

class AWS4AuthPlugin:
    """AWS Signature Version 4 authentication plugin."""
    
    def __init__(self, access_key: str, secret_key: str, region: str, service: str):
        self.credentials = botocore.credentials.Credentials(access_key, secret_key)
        self.region = region
        self.service = service

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        try:
            parsed_url = urlparse(request.url)
            signer = botocore.auth.SigV4Auth(self.credentials, self.service, self.region)
            headers = signer.add_auth(
                request=request.method,
                uri=parsed_url.path or '/',
                querystring=request.params or {},
                headers=request.headers,
                body=request.data or b'',
                date=datetime.datetime.now(timezone.utc),
            )
            request.headers.update(headers)
            return request
        except Exception as e:
            raise AuthError(f"AWS4 authentication failed: {str(e)}") from e