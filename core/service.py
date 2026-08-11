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

    def is_dvx_process(self, pid: int):
        """
        Проверяет, что PID принадлежит именно DataVisionX daemon.
        """
        try:
            cmdline = Path(f"/proc/{pid}/cmdline").read_bytes()
            cmdline = cmdline.replace(b"\\x00", b" ").decode(
                "utf-8", errors="ignore"
            )
            return "core.daemon" in cmdline
        except Exception:
            return False

    def is_running(self):
        """
        Проверяет, работает ли Runtime.
        """
        pid = self.read_pid()

        if pid is None:
            return False

        if not self.pid_exists(pid):
            self.remove_pid()
            return False

        if not self.is_dvx_process(pid):
            self.remove_pid()
            return False

        return True

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
        Останавливает именно DataVisionX daemon
        и подтверждает фактическое завершение процесса.
        """
        pid = self.read_pid()

        if pid is None:
            return False

        if not self.pid_exists(pid):
            self.remove_pid()
            return False

        if not self.is_dvx_process(pid):
            self.remove_pid()
            return False

        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            self.remove_pid()
            return False
        except PermissionError:
            return False

        import time

        # Даём процессу до 5 секунд на штатное завершение.
        for _ in range(50):
            if not self.pid_exists(pid):
                self.remove_pid()
                return True
            time.sleep(0.1)

        # Если SIGTERM не помог — принудительное завершение.
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            self.remove_pid()
            return True
        except PermissionError:
            return False

        # Подтверждаем завершение после SIGKILL.
        for _ in range(20):
            if not self.pid_exists(pid):
                self.remove_pid()
                return True
            time.sleep(0.1)

        return False


service = ServiceManager()
