from abc import ABC, abstractmethod
from ..request import NeoVortexRequest

class AuthBase(ABC):
    """Base class for authentication handlers."""
    
    @abstractmethod
    def apply(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Apply authentication to the request (legacy method)."""
        pass
    
    def authenticate(self, request: NeoVortexRequest) -> NeoVortexRequest:
        """Apply authentication to the request.
        
        By default, this calls the apply method for backward compatibility.
        Subclasses can override this method if needed.
        """
        return self.apply(request)