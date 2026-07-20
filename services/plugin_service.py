from core.plugins import plugin_manager


class PluginService:
    """Service for managing DataVision X plugins."""

    def load(self):
        plugin_manager.load_plugins()

    def list(self):
        return plugin_manager.list_plugins()

    def count(self):
        return plugin_manager.count()


plugin_service = PluginService()
