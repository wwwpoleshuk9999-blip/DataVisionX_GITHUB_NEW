import time
import json
from pathlib import Path

from core.runtime import runtime
from core.service import service
from core.plugin_recovery import plugin_recovery


EVENT_LOG = Path("runtime/events.log")
RECOVERY_LOG = Path("runtime/recovery.log")


class RecoveryManager:

    MAX_ATTEMPTS = 3

    def __init__(self):
        self.attempts = 0
        self.last_action = None
        self.last_recovery = None
        self.history = []

    def write_event(self, action, data=None):

        event = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "source": "recovery",
            "user": "system",
            "data": data or {}
        }

        EVENT_LOG.parent.mkdir(exist_ok=True)

        with EVENT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


        with RECOVERY_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


        self.history.append(event)

        self.last_action = action
        self.last_recovery = int(time.time())


    def status(self):

        return {
            "last_action": self.last_action,
            "last_recovery": self.last_recovery,
            "attempts": self.attempts,
            "history_count": len(self.history)
        }


    def get_history(self):

        return self.history[-50:]


    def check_and_recover(self):

        runtime_data = runtime.read()
        process_running = service.is_running()

        healthy = (
            runtime_data.get("status") == "RUNNING"
            and process_running
        )


        if healthy:
            return {
                "status": "OK",
                "action": None,
                "attempts": self.attempts,
                "last_recovery": self.last_recovery
            }


        if self.attempts >= self.MAX_ATTEMPTS:

            self.write_event(
                "RECOVERY_LIMIT_REACHED"
            )

            return {
                "status": "FAILED",
                "attempts": self.attempts
            }


        self.attempts += 1

        self.write_event(
            "RECOVERY_STARTED"
        )


        recovered = plugin_recovery.recover()


        self.write_event(
            "RECOVERY_SUCCESS",
            {
                "plugins": recovered
            }
        )


        self.attempts = 0


        return {
            "status": "RECOVERED",
            "plugins": recovered,
            "last_recovery": self.last_recovery
        }


recovery = RecoveryManager()
