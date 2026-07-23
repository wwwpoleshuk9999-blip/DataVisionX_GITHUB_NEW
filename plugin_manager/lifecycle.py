import importlib


class PluginLifecycle:

    def __init__(self):
        self.instances = {}

    def start(self, plugin):

        module = importlib.import_module(
            f"plugins.{plugin.id}.plugin"
        )

        plugin_class = getattr(
            module,
            "Plugin"
        )

        instance = plugin_class()

        if hasattr(instance, "start"):
            instance.start()

        self.instances[plugin.id] = instance

        return instance

    def stop(self, plugin_id):

        instance = self.instances.get(plugin_id)

        if not instance:
            return False

        if hasattr(instance, "stop"):
            instance.stop()

        del self.instances[plugin_id]

        return True
