from typing import Dict, Callable, Any
from .request import NeoVortexRequest
from .response import NeoVortexResponse

class HookManager:
    """Manages event hooks for request/response lifecycle."""
    
    def __init__(self):
        self.hooks: Dict[str, list[Callable]] = {
            "pre_request": [],
            "post_response": [],
        }

    def register(self, event: str, callback: Callable):
        if event in self.hooks:
            self.hooks[event].append(callback)

    def run(self, event: str, data: Any):
        for callback in self.hooks.get(event, []):
            callback(data)