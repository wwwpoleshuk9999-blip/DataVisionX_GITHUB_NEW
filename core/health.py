import time
import json
from pathlib import Path


STATE_FILE = Path("runtime/state.json")


class HealthMonitor:
    def __init__(self):
        self.start_time = None
        self.status = "STOPPED"

    def save(self):
        STATE_FILE.parent.mkdir(exist_ok=True)

        uptime = 0

        if self.start_time:
            uptime = int(time.time() - self.start_time)

        with open(STATE_FILE, "w") as file:
            json.dump(
                {
                    "status": self.status,
                    "uptime": uptime
                },
                file,
                indent=4
            )

    def start(self):
        self.start_time = time.time()
        self.status = "RUNNING"
        self.save()

    def stop(self):
        self.status = "STOPPED"
        self.save()

    def report(self):
        if STATE_FILE.exists():
            with open(STATE_FILE, "r") as file:
                return json.load(file)

        return {
            "status": "UNKNOWN",
            "uptime": 0
        }


health = HealthMonitor()
