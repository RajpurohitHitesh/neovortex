from typing import List
from .request import NeoVortexRequest
import pickle
import os

class OfflineHandler:
    """Handles offline request queuing."""
    
    def __init__(self, queue_file: str = "offline_queue.pkl"):
        self.queue_file = queue_file
        self.queue: List[NeoVortexRequest] = self._load_queue()

    def _load_queue(self) -> List[NeoVortexRequest]:
        if os.path.exists(self.queue_file):
            with open(self.queue_file, "rb") as f:
                return pickle.load(f)
        return []

    def _save_queue(self):
        with open(self.queue_file, "wb") as f:
            pickle.dump(self.queue, f)

    def queue_request(self, request: NeoVortexRequest):
        self.queue.append(request)
        self._save_queue()

    def retry_requests(self, client):
        for request in self.queue:
            try:
                client.request(
                    method=request.method,
                    url=request.url,
                    params=request.params,
                    data=request.data,
                    json=request.json,
                    files=request.files,
                    headers=request.headers,
                )
                self.queue.remove(request)
            except Exception:
                continue
        self._save_queue()