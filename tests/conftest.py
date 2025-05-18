import pytest
from neovortex.plugins.metrics import MetricsPlugin

@pytest.fixture(autouse=True)
def clear_prometheus_registry():
    """Clear Prometheus registry before each test."""
    MetricsPlugin().clear_metrics()
    yield