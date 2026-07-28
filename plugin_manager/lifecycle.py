import importlib
from core.runtime import runtime


class PluginLifecycle:

    def __init__(self, event_bus=None):
        self.instances = {}
        self.event_bus = event_bus


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

            print("LIFECYCLE EVENT: plugin_started", plugin.id)

            event_bus = self.event_bus or runtime.get_service("event_bus")

            if event_bus:
                print("EVENT BUS FOUND")

                event_bus.emit(
                    "system",
                    "plugin_started",
                    {
                        "plugin": plugin.id,
                        "status": "RUNNING"
                    }
                )
            else:
                print("EVENT BUS MISSING")

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

            event_bus = self.event_bus or runtime.get_service("event_bus")

            if event_bus:
                event_bus.emit(
                    "system",
                    "plugin_stopped",
                    {
                        "plugin": plugin_id,
                        "status": "STOPPED"
                    }
                )

            return True

        except Exception as e:
            print(
                f"Plugin stop error: {e}"
            )
            return False
