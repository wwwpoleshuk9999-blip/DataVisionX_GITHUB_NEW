import os
from datetime import datetime


EVENT_LOG = "runtime/events.log"


class EventBus:

    def __init__(self, permission_manager):

        self.permissions = permission_manager
        self.listeners = {}


    def register(self, plugin_id, event, callback):

        if not self.permissions.require(
            plugin_id,
            "events"
        ):
            return False


        if event not in self.listeners:

            self.listeners[event] = []


        self.listeners[event].append(
            {
                "plugin": plugin_id,
                "callback": callback
            }
        )

        self.log(
            f"{plugin_id} registered {event}"
        )

        return True



    def emit(self, plugin_id, event, data=None):

        if not self.permissions.require(
            plugin_id,
            "events"
        ):
            return False


        self.log(
            f"{plugin_id} emitted {event}"
        )


        for listener in self.listeners.get(
            event,
            []
        ):

            try:

                listener["callback"](
                    data
                )

            except Exception as e:

                self.log(
                    f"ERROR {listener['plugin']} {e}"
                )


        return True



    def log(self, message):

        os.makedirs(
            "runtime",
            exist_ok=True
        )

        with open(
            EVENT_LOG,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{datetime.now()} | {message}\n"
            )
