from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse
from neovortex.exceptions import NeoVortexError
import sentry_sdk

class SentryPlugin:
    """Integrates with Sentry for error tracking and performance monitoring."""
    
    def __init__(self, dsn: str, environment: str = "production"):
        try:
            sentry_sdk.init(
                dsn=dsn,
                environment=environment,
                traces_sample_rate=1.0,
            )
        except Exception as e:
            raise NeoVortexError(f"Sentry initialization failed: {str(e)}")

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        with sentry_sdk.start_transaction(op="http", name=f"{request.method} {request.url}"):
            return request

    def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse:
        if response.status_code >= 400:
            sentry_sdk.capture_message(
                f"HTTP {response.status_code} on {request.method} {request.url}"
            )
        return response

    def capture_exception(self, exception: Exception):
        sentry_sdk.capture_exception(exception)