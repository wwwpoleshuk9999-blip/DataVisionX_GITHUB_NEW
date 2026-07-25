import time
import json
from pathlib import Path

from core.runtime import runtime
from core.service import service


WATCHDOG_LOG = Path("runtime/watchdog.log")
EVENT_LOG = Path("runtime/events.log")


class Watchdog:

    def __init__(self):
        self.last_check = None
        self.status = "INIT"
        self.last_event = None

    def write_json_log(self, file, data):

        file.parent.mkdir(exist_ok=True)

        with file.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(data, ensure_ascii=False)
                + "\n"
            )

    def write_event(self, action):

        event = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "source": "watchdog",
            "user": "system"
        }

        self.write_json_log(
            EVENT_LOG,
            event
        )

        self.last_event = action

    def check(self):

        runtime_data = runtime.read()

        process_running = service.is_running()

        if process_running and runtime_data.get("status") == "RUNNING":

            self.status = "HEALTHY"

            action = "WATCHDOG_HEALTHY"

        else:

            self.status = "WARNING"

            action = "WATCHDOG_WARNING"


        self.last_check = int(time.time())

        result = {
            "status": self.status,
            "runtime": runtime_data.get("status"),
            "process": "RUNNING" if process_running else "STOPPED",
            "pid": service.read_pid(),
            "checked_at": self.last_check
        }

        self.write_json_log(
            WATCHDOG_LOG,
            result
        )

        self.write_event(action)

        return result


watchdog = Watchdog()
