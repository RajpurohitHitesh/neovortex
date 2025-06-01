"""
NeoVortex Rate Limiter
=====================

This module provides rate limiting capabilities to prevent API abuse
and respect server-imposed rate limits.
"""

# Re-export RateLimiter from utils.rate_limiter
from .utils.rate_limiter import RateLimiter

# Export symbols for better import management
__all__ = ['RateLimiter']