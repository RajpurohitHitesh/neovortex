import pytest
from neovortex.utils.rate_limiter import RateLimiter
from neovortex.exceptions import RateLimitError
from neovortex.request import NeoVortexRequest

def test_rate_limiter():
    limiter = RateLimiter(requests_per_second=1, bucket_size=1)
    request = NeoVortexRequest("GET", "https://example.com")
    limiter.check_limit(request)  # First request should pass
    with pytest.raises(RateLimitError):
        limiter.check_limit(request)  # Second request should fail due to rate limit