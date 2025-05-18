from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse
from neovortex.exceptions import NeoVortexError
import xmltodict
import json

class XMLToJSONPlugin:
    """Converts XML responses to JSON."""
    
    def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse:
        content_type = response.headers.get("Content-Type", "")
        if "xml" in content_type.lower() and response.text:
            try:
                xml_data = xmltodict.parse(response.text)
                response.json_data = json.loads(json.dumps(xml_data))
                response.text = json.dumps(response.json_data)
                response.content = response.text.encode("utf-8")
                response.headers["Content-Type"] = "application/json"
            except Exception as e:
                raise NeoVortexError(f"XML to JSON conversion failed: {str(e)}")
        return response