import importlib


class PluginLifecycle:

    def __init__(self):
        self.instances = {}


    def start(self, plugin):

        try:
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

            plugin.status = "RUNNING"

            return instance

        except Exception as e:
            print(
                f"Plugin start error: {e}"
            )
            return None


    def stop(self, plugin_id):

        instance = self.instances.get(plugin_id)

        if not instance:
            return False

        try:
            if hasattr(instance, "stop"):
                instance.stop()

            del self.instances[plugin_id]

            return True

        except Exception as e:
            print(
                f"Plugin stop error: {e}"
            )
            return False
