from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse
from neovortex.exceptions import NeoVortexError
import time
import statistics

class DynamicThrottlePlugin:
    """Dynamically adjusts request rates based on server feedback."""
    
    def __init__(self, initial_rps: float = 10.0, min_rps: float = 1.0, max_rps: float = 100.0):
        self.rps = initial_rps
        self.min_rps = min_rps
        self.max_rps = max_rps
        self.latencies = []
        self.last_request = 0.0

    def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse, start_time: float) -> NeoVortexResponse:
        latency = time.time() - start_time
        self.latencies.append(latency)
        if len(self.latencies) > 10:
            self.latencies.pop(0)
        if len(self.latencies) >= 5:
            avg_latency = statistics.mean(self.latencies)
            if avg_latency > 1.0:  # High latency, reduce rate
                self.rps = max(self.min_rps, self.rps * 0.8)
            elif avg_latency < 0.2:  # Low latency, increase rate
                self.rps = min(self.max_rps, self.rps * 1.2)
        return response

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        now = time.time()
        if now - self.last_request < 1.0 / self.rps:
            time.sleep(1.0 / self.rps - (now - self.last_request))
        self.last_request = time.time()
        return request