from plugin_manager.manager import plugin_manager


class PluginService:
    """Service for managing DataVision X plugins."""

    def load(self):
        plugin_manager.discover()

    def list(self):
        return plugin_manager.list_plugins()

    def count(self):
        return len(plugin_manager.list_plugins())


plugin_service = PluginService()
