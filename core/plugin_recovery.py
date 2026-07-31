import time
import json
from pathlib import Path

from plugin_manager.manager import plugin_manager
from core.runtime import runtime

EVENT_LOG = Path("runtime/events.log")


class PluginRecovery:

    def write_event(self, action, plugin_id):

        EVENT_LOG.parent.mkdir(exist_ok=True)

        event = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "plugin": plugin_id,
            "source": "plugin_recovery",
            "user": "system"
        }

        with EVENT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def recover(self):

        recovered = []

        plugin_manager.discover()

        for plugin in plugin_manager.plugins.values():

            if plugin.status != "RUNNING":

                if plugin_manager.start(plugin.id):

                    self.write_event(
                        "PLUGIN_RECOVERY_SUCCESS",
                        plugin.id
                    )

                    health = getattr(
                        plugin_manager,
                        "health",
                        None
                    )

                    if health:
                        health.recovered(plugin.id)

                    event_bus = runtime.get_service(
                        "event_bus"
                    )

                    if event_bus:
                        event_bus.emit(
                            "system",
                            "plugin_recovered",
                            {
                                "plugin": plugin.id,
                                "status": "RUNNING"
                            }
                        )

                    recovered.append(plugin.id)

        return recovered


plugin_recovery = PluginRecovery()
