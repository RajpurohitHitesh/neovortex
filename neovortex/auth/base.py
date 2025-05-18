from abc import ABC, abstractmethod
from ..request import NeoVortexRequest

class AuthBase(ABC):
    """Base class for authentication handlers."""
    
    @abstractmethod
    def apply(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Apply authentication to the request."""
        pass