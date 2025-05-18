from typing import Optional
from pydantic import BaseModel, ValidationError
from jsonschema import validate, ValidationError as JSONSchemaValidationError
from ..request import NeoVortexRequest
from ..response import NeoVortexResponse
from ..exceptions import NeoVortexError

class RequestValidator:
    """Validates requests and responses using Pydantic or JSON Schema."""
    
    def __init__(self, pydantic_schema: Optional[BaseModel] = None, json_schema: Optional[dict] = None):
        self.pydantic_schema = pydantic_schema
        self.json_schema = json_schema
        if not (pydantic_schema or json_schema):
            raise NeoVortexError("At least one schema (Pydantic or JSON Schema) required")

    def validate_request(self, request: NeoVortexRequest):
        data = request.json or request.data or {}
        if self.pydantic_schema:
            try:
                self.pydantic_schema(**data)
            except ValidationError as e:
                raise NeoVortexError(f"Pydantic request validation failed: {str(e)}")
        if self.json_schema:
            try:
                validate(instance=data, schema=self.json_schema)
            except JSONSchemaValidationError as e:
                raise NeoVortexError(f"JSON Schema request validation failed: {str(e)}")

    def validate_response(self, response: NeoVortexResponse):
        if response.json_data:
            if self.pydantic_schema:
                try:
                    self.pydantic_schema(**response.json_data)
                except ValidationError as e:
                    raise NeoVortexError(f"Pydantic response validation failed: {str(e)}")
            if self.json_schema:
                try:
                    validate(instance=response.json_data, schema=self.json_schema)
                except JSONSchemaValidationError as e:
                    raise NeoVortexError(f"JSON Schema response validation failed: {str(e)}")