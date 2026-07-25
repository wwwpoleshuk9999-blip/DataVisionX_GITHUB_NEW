from plugin_manager.loader import PluginLoader
from plugin_manager.validator import PluginValidator
from plugin_manager.lifecycle import PluginLifecycle
from plugin_manager.installer import PluginInstaller

from core.plugin_registry import register_plugin


class PluginManager:

    def __init__(self):
        self.loader = PluginLoader()
        self.validator = PluginValidator()
        self.lifecycle = PluginLifecycle()
        self.installer = PluginInstaller()
        self.plugins = {}

    def discover(self):
        discovered = {}

        for plugin in self.loader.discover():

            valid, errors = self.validator.validate(plugin)

            if valid:

                if plugin.id in self.plugins:
                    plugin.status = self.plugins[plugin.id].status
                else:
                    plugin.status = getattr(plugin, "status", "STOPPED")

                discovered[plugin.id] = plugin

                register_plugin(
                    plugin.id,
                    plugin.name,
                    plugin.version,
                    getattr(plugin, "path", "")
                )

            else:
                print(f"{plugin.id}: {errors}")

        self.plugins = discovered
        return list(self.plugins.values())

    def list_plugins(self):
        return list(self.plugins.values())

    def get_plugin(self, plugin_id):
        return self.plugins.get(plugin_id)

    def start(self, plugin_id):
        self.discover()

        plugin = self.plugins.get(plugin_id)

        if not plugin:
            return False

        try:
            instance = self.lifecycle.start(plugin)

            if instance:
                plugin.status = "RUNNING"
                return True

        except Exception as e:
            print("START ERROR:", e)

        return False

    def stop(self, plugin_id):

        plugin = self.plugins.get(plugin_id)

        if not plugin:
            return False

        try:
            result = self.lifecycle.stop(plugin_id)

            if result:
                plugin.status = "STOPPED"

            return result

        except Exception as e:
            print("STOP ERROR:", e)

        return False

    def restart(self, plugin_id):

        plugin = self.plugins.get(plugin_id)

        if not plugin:
            return False

        try:
            self.lifecycle.stop(plugin_id)

            instance = self.lifecycle.start(plugin)

            if instance:
                plugin.status = "RUNNING"
                return True

        except Exception as e:
            print("RESTART ERROR:", e)

        return False

    def install(self, plugin):
        return self.installer.install(plugin)

    def remove(self, plugin_id):

        if plugin_id in self.plugins:
            del self.plugins[plugin_id]
            return True

        return False


plugin_manager = PluginManager()
