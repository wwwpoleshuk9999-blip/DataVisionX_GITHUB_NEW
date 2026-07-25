import os
import signal
from pathlib import Path


PID_FILE = Path("runtime/dvx.pid")


class ServiceManager:
    def __init__(self):
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)

    def save_pid(self, pid: int | None = None):
        """
        Сохраняет PID текущего процесса или указанный PID.
        """
        if pid is None:
            pid = os.getpid()

        PID_FILE.write_text(str(pid), encoding="utf-8")

    def read_pid(self):
        """
        Возвращает PID из файла.
        """
        if not PID_FILE.exists():
            return None

        try:
            value = PID_FILE.read_text(encoding="utf-8").strip()

            if not value:
                return None

            return int(value)

        except Exception:
            return None

    def remove_pid(self):
        """
        Удаляет PID файл.
        """
        if PID_FILE.exists():
            PID_FILE.unlink()

    def pid_exists(self, pid: int):
        """
        Проверяет существование процесса.
        """
        try:
            os.kill(pid, 0)
            return True

        except ProcessLookupError:
            return False

        except PermissionError:
            return True

        except Exception:
            return False

    def is_running(self):
        """
        Проверяет, работает ли Runtime.
        """
        pid = self.read_pid()

        if pid is None:
            return False

        if self.pid_exists(pid):
            return True

        # PID устарел
        self.remove_pid()
        return False

    def ensure_pid(self):
        """
        Создаёт PID файл при необходимости.
        """
        if not self.is_running():
            self.save_pid()

    def status(self):
        """
        Возвращает расширенную информацию.
        """
        pid = self.read_pid()

        return {
            "running": self.is_running(),
            "pid": pid,
            "pid_file": str(PID_FILE),
            "exists": PID_FILE.exists(),
        }

    def stop(self):
        """
        Останавливает процесс.
        """
        pid = self.read_pid()

        if pid is None:
            return False

        try:
            os.kill(pid, signal.SIGTERM)

        except ProcessLookupError:
            pass

        except PermissionError:
            return False

        finally:
            self.remove_pid()

        return True


service = ServiceManager()
