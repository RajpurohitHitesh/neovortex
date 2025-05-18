from prometheus_client import Counter, Histogram, Gauge, REGISTRY
from ..request import NeoVortexRequest
from ..response import NeoVortexResponse
import time

class MetricsPlugin:
    """Plugin for collecting detailed performance metrics."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsPlugin, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.requests_total = Counter(
                "neovortex_requests_total", "Total HTTP requests", ["method", "endpoint"]
            )
            self.request_latency = Histogram(
                "neovortex_request_latency_seconds", "Request latency", ["method", "endpoint"]
            )
            self.error_count = Counter(
                "neovortex_errors_total", "Total request errors", ["method", "endpoint", "status_code"]
            )
            self.active_requests = Gauge(
                "neovortex_active_requests", "Number of active requests"
            )
            self._initialized = True

    def track_request(self, request: NeoVortexRequest, response: NeoVortexResponse, start_time: float):
        endpoint = request.url.split("?")[0]
        labels = {"method": request.method, "endpoint": endpoint}
        self.requests_total.labels(**labels).inc()
        self.request_latency.labels(**labels).observe(time.time() - start_time)
        self.active_requests.dec()
        if response.status_code >= 400:
            self.error_count.labels(
                method=request.method,
                endpoint=endpoint,
                status_code=str(response.status_code)
            ).inc()

    def track_start(self):
        self.active_requests.inc()

    def clear_metrics(self):
        """Clear all metrics from the registry."""
        for collector in list(REGISTRY._collector_to_names):
            REGISTRY.unregister(collector)