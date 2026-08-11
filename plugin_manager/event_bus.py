import os
import copy
from datetime import datetime


EVENT_LOG = "runtime/events.log"


class EventBus:

    def __init__(self, permission_manager):

        self.permissions = permission_manager
        self.listeners = {}


    def register(self, plugin_id, event, callback):
        if not callable(callback):
            return False

        if plugin_id != "system" and not self.permissions.require(
            plugin_id,
            "events"
        ):
            return False

        if event not in self.listeners:
            self.listeners[event] = []

        for listener in self.listeners[event]:
            if listener["plugin"] == plugin_id:
                return True

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

    def unregister(self, plugin_id, event, callback):
        if not callable(callback):
            return False

        if plugin_id != "system" and not self.permissions.require(
            plugin_id,
            "events"
        ):
            return False

        listeners = self.listeners.get(event, [])

        for index, listener in enumerate(listeners):
            existing = listener["callback"]

            same_callback = existing is callback

            if (
                hasattr(existing, "__self__")
                and hasattr(existing, "__func__")
                and hasattr(callback, "__self__")
                and hasattr(callback, "__func__")
            ):
                same_callback = (
                    existing.__self__ is callback.__self__
                    and existing.__func__ is callback.__func__
                )

            if (
                listener["plugin"] == plugin_id
                and same_callback
            ):
                del listeners[index]

                if not listeners:
                    self.listeners.pop(event, None)

                self.log(
                    f"{plugin_id} unregistered {event}"
                )

                return True

        return False


    def emit(self, plugin_id, event, data=None):

        if not self.permissions.require(
            plugin_id,
            "events"
        ):
            return False


        self.log(
            f"{plugin_id} emitted {event}"
        )


        listeners_snapshot = list(
            self.listeners.get(
                event,
                []
            )
        )

        for listener in listeners_snapshot:

            try:

                listener["callback"](
                    {
                        "event": event,
                        "source": plugin_id,
                        "data": copy.deepcopy(data)
                    }
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
