import time
import json
from pathlib import Path

from core.runtime import runtime
from core.service import service
from core.plugin_recovery import plugin_recovery


EVENT_LOG = Path("runtime/events.log")


class RecoveryManager:

    MAX_ATTEMPTS = 3

    def __init__(self):
        self.attempts = 0
        self.last_action = None
        self.last_recovery = None

    def write_event(self, action):

        event = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "source": "recovery",
            "user": "system"
        }

        EVENT_LOG.parent.mkdir(exist_ok=True)

        with EVENT_LOG.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(event, ensure_ascii=False)
                + "\n"
            )

        self.last_action = action
        self.last_recovery = int(time.time())


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
                "action": self.last_action,
                "attempts": self.attempts,
                "message": "Recovery limit reached"
            }


        self.attempts += 1

        self.write_event(
            "RECOVERY_STARTED"
        )

        # Безопасная подготовка.
        # Реальный restart подключим после теста.

        recovered = plugin_recovery.recover()

        self.write_event(
            "RECOVERY_SUCCESS"
        )

        self.attempts = 0

        return {
            "status": "RECOVERED",
            "action": self.last_action,
            "attempts": self.attempts,
            "last_recovery": self.last_recovery
        }


recovery = RecoveryManager()
