class PluginRegistry:
    """Manages enabling/disabling of plugins."""
    def __init__(self):
        self.plugins = {}
        self.enabled = set()
        self._initialized = False

    def _initialize_plugins(self):
        """Initialize default plugins."""
        if not self._initialized:
            try:
                from .caching import CachePlugin
                from .logging import LoggingPlugin
                from .metrics import MetricsPlugin
                from .custom.etag_cache import ETagCachePlugin
                from .custom.compression import CompressionPlugin
                from .custom.xml_to_json import XMLToJSONPlugin
                from .custom.dynamic_throttle import DynamicThrottlePlugin
                from .custom.graphql import GraphQLPlugin
                
                self.register("cache", CachePlugin())
                self.register("logging", LoggingPlugin())
                self.register("metrics", MetricsPlugin())
                # AWS4AuthPlugin, APIKeyRotationPlugin, SentryPlugin, and CDNProxyPlugin 
                # require specific parameters, register only when explicitly enabled
                self.register("etag_cache", ETagCachePlugin())
                self.register("compression", CompressionPlugin())
                self.register("xml_to_json", XMLToJSONPlugin())
                self.register("dynamic_throttle", DynamicThrottlePlugin())
                self.register("graphql", GraphQLPlugin())
                self._initialized = True
            except ImportError as e:
                # Log error but don't crash when a plugin is missing
                import logging
                logging.getLogger("neovortex").warning(f"Plugin initialization error: {str(e)}")

    def register(self, plugin_name: str, plugin_instance):
        """Register a plugin with the registry."""
        self.plugins[plugin_name] = plugin_instance

    def enable(self, plugin_name: str):
        """Enable a plugin by name."""
        self._initialize_plugins()
        if plugin_name in ("aws4_auth", "api_key_rotation", "sentry", "cdn_proxy") and plugin_name not in self.plugins:
            raise ValueError(f"{plugin_name} requires manual registration with required parameters")
        if plugin_name in self.plugins:
            self.enabled.add(plugin_name)
        else:
            raise ValueError(f"Plugin {plugin_name} not found")

    def disable(self, plugin_name: str):
        """Disable a plugin by name."""
        self.enabled.discard(plugin_name)

    def get(self, plugin_name: str):
        """Get a plugin by name if it's enabled."""
        self._initialize_plugins()
        if plugin_name in self.enabled:
            return self.plugins.get(plugin_name)
        return None

# Singleton instance
registry = PluginRegistry()

# Export symbols
__all__ = ['PluginRegistry', 'registry']