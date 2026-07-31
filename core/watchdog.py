import time
import json
from pathlib import Path

from core.runtime import runtime
from core.service import service
from core.recovery import recovery


WATCHDOG_LOG = Path("runtime/watchdog.log")
EVENT_LOG = Path("runtime/events.log")


class Watchdog:

    def __init__(self):
        self.last_check = None
        self.status = "INIT"
        self.last_event = None
        self.history = []
        self.warning_count = 0
        self.healthy_count = 0

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

    def status_info(self):

        return {
            "status": self.status,
            "last_check": self.last_check,
            "last_event": self.last_event,
            "warning_count": self.warning_count,
            "healthy_count": self.healthy_count,
            "history_count": len(self.history)
        }


    def get_history(self):

        return self.history[-50:]


    def check(self):

        runtime_data = runtime.read()

        process_running = service.is_running()

        if process_running and runtime_data.get("status") == "RUNNING":

            self.status = "HEALTHY"

            action = "WATCHDOG_HEALTHY"

        else:

            self.status = "WARNING"

            action = "WATCHDOG_WARNING"

            recovery_result = recovery.check_and_recover()


        self.last_check = int(time.time())

        if self.status == "WARNING":
            self.warning_count += 1
        else:
            self.healthy_count += 1

        result = {
            "status": self.status,
            "runtime": runtime_data.get("status"),
            "process": "RUNNING" if process_running else "STOPPED",
            "pid": service.read_pid(),
            "checked_at": self.last_check
        }

        if self.status == "WARNING" and recovery_result:
            result["recovery"] = recovery_result

        self.write_json_log(
            WATCHDOG_LOG,
            result
        )

        self.write_event(action)

        self.history.append(result)

        return result


watchdog = Watchdog()
