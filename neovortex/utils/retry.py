import secrets
import time
from typing import Callable, TypeVar, Any
from ..exceptions import NeoVortexError

T = TypeVar('T')

class RetryHandler:
    """Handles retry logic with exponential backoff and jitter."""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def retry(self, func: Callable[..., T], *args, **kwargs) -> T:
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise NeoVortexError(f"Retry failed after {self.max_retries} attempts: {str(e)}") from e
                delay = self.base_delay * (2 ** attempt) + secrets.randbelow(100) / 1000.0
                time.sleep(delay)
        return None  # Unreachable, but mypy needs it