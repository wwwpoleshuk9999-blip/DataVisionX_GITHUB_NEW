from plugin_manager.loader import PluginLoader
from plugin_manager.validator import PluginValidator
from plugin_manager.lifecycle import PluginLifecycle
from plugin_manager.installer import PluginInstaller


class PluginManager:

    def __init__(self):

        self.loader = PluginLoader()
        self.validator = PluginValidator()
        self.lifecycle = PluginLifecycle()
        self.installer = PluginInstaller()

        self.plugins = {}

    def discover(self):

        self.plugins = {}

        for plugin in self.loader.discover():

            valid, errors = self.validator.validate(plugin)

            if valid:

                self.plugins[plugin.id] = plugin

            else:

                print(f"{plugin.id}: {errors}")

        return self.plugins

    def start(self, plugin_id):

        plugin = self.plugins.get(plugin_id)

        if not plugin:
            return False

        self.lifecycle.start(plugin)

        return True

    def stop(self, plugin_id):

        return self.lifecycle.stop(plugin_id)


plugin_manager = PluginManager()
