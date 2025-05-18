import logging
from typing import Optional
from datetime import datetime, timezone
from ..request import NeoVortexRequest
from ..response import NeoVortexResponse
import elasticsearch

class LoggingPlugin:
    """Plugin for logging requests and responses to multiple sinks."""
    
    def __init__(
        self,
        logger_name: str = "neovortex",
        level: str = "INFO",
        elasticsearch_url: Optional[str] = None
    ):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.es_client = None
        if elasticsearch_url:
            try:
                self.es_client = elasticsearch.Elasticsearch([elasticsearch_url])
            except Exception as e:
                self.logger.warning(f"Elasticsearch connection failed: {str(e)}")

    def log_request(self, request: NeoVortexRequest):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": request.method,
            "url": request.url,
            "headers": dict(request.headers),
        }
        self.logger.info(f"Request: {log_data}")
        if self.es_client:
            try:
                self.es_client.index(index="neovortex_requests", body=log_data)
            except Exception as e:
                self.logger.warning(f"Elasticsearch logging failed: {str(e)}")

    def log_response(self, response: NeoVortexResponse):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status_code": response.status_code,
            "headers": dict(response.headers),
        }
        self.logger.info(f"Response: {log_data}")
        if self.es_client:
            try:
                self.es_client.index(index="neovortex_responses", body=log_data)
            except Exception as e:
                self.logger.warning(f"Elasticsearch logging failed: {str(e)}")