import json
import time
from pathlib import Path


STATE_FILE = Path("runtime/state.json")


class RuntimeManager:
    def __init__(self):
        STATE_FILE.parent.mkdir(exist_ok=True)

        if not STATE_FILE.exists():
            self._save({
                "status": "STOPPED",
                "started_at": 0
            })

    def _load(self):
        if not STATE_FILE.exists():
            return {
                "status": "STOPPED",
                "started_at": 0
            }

        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))

        # Автоматическая миграция старого формата
        if "started_at" not in data:
            status = data.get("status", "STOPPED")

            if status == "RUNNING":
                started_at = int(time.time())
            else:
                started_at = 0

            data = {
                "status": status,
                "started_at": started_at
            }

            self._save(data)

        return data

    def _save(self, data):
        STATE_FILE.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

    def read(self):
        return self._load()

    def start(self):
        self._save({
            "status": "RUNNING",
            "started_at": int(time.time())
        })

    def stop(self):
        self._save({
            "status": "STOPPED",
            "started_at": 0
        })

    def uptime(self):
        data = self._load()

        if data["status"] != "RUNNING":
            return 0

        return max(0, int(time.time()) - data["started_at"])


runtime = RuntimeManager()
