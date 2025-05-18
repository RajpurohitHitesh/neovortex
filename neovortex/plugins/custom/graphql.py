from typing import Optional
from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse
from neovortex.exceptions import NeoVortexError
from graphql import parse, validate, build_schema
import json

class GraphQLPlugin:
    """Simplifies GraphQL queries with schema validation and batching."""
    
    def __init__(self, schema_sdl: Optional[str] = None):
        self.schema = build_schema(schema_sdl) if schema_sdl else None

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        if request.json and "query" in request.json:
            query = request.json["query"]
            try:
                parsed_query = parse(query)
                if self.schema:
                    errors = validate(self.schema, parsed_query)
                    if errors:
                        raise NeoVortexError(f"GraphQL query validation failed: {errors}")
            except Exception as e:
                raise NeoVortexError(f"GraphQL query parsing failed: {str(e)}")
        return request

    def batch_queries(self, queries: list[dict]) -> dict:
        """Combine multiple GraphQL queries into a single request."""
        return {"queries": queries}