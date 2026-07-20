import os
import signal
from pathlib import Path


PID_FILE = Path("runtime/dvx.pid")


class ServiceManager:
    def __init__(self):
        PID_FILE.parent.mkdir(exist_ok=True)

    def save_pid(self, pid: int):
        PID_FILE.write_text(str(pid), encoding="utf-8")

    def read_pid(self):
        if not PID_FILE.exists():
            return None

        value = PID_FILE.read_text(encoding="utf-8").strip()

        if not value:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    def remove_pid(self):
        if PID_FILE.exists():
            PID_FILE.unlink()

    def is_running(self):
        pid = self.read_pid()

        if pid is None:
            return False

        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            self.remove_pid()
            return False
        except PermissionError:
            return True

    def status(self):
        return {
            "running": self.is_running(),
            "pid": self.read_pid(),
        }

    def stop(self):
        pid = self.read_pid()

        if pid is None:
            return False

        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

        self.remove_pid()
        return True


service = ServiceManager()
