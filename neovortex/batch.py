from typing import List, Dict, Any, Optional
from .async_client import AsyncNeoVortexClient
from .response import NeoVortexResponse
from .exceptions import NeoVortexError

class BatchHandler:
    """Handles batching and aggregation of requests with API-specific support."""
    
    def __init__(self, client: AsyncNeoVortexClient, batch_endpoint: Optional[str] = None):
        self.client = client
        self.batch_endpoint = batch_endpoint

    async def process_batch(self, requests: List[Dict[str, Any]]) -> List[NeoVortexResponse]:
        """Process a batch of requests, using batch endpoint if provided."""
        if self.batch_endpoint:
            try:
                batch_request = {"requests": requests}
                response = await self.client.request(
                    method="POST",
                    url=self.batch_endpoint,
                    json=batch_request,
                )
                if response.json_data and "responses" in response.json_data:
                    return [NeoVortexResponse(r) for r in response.json_data["responses"]]
                raise NeoVortexError("Invalid batch response format")
            except Exception as e:
                raise NeoVortexError(f"Batch request failed: {str(e)}") from e
        return await self.client.batch_requests(requests)

    async def aggregate(self, responses: List[NeoVortexResponse]) -> Dict[str, Any]:
        """Aggregate responses into a structured format."""
        return {
            f"response_{i}": resp.json_data or resp.text
            for i, resp in enumerate(responses)
        }