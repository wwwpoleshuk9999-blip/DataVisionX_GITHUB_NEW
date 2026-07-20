import sys
import subprocess
from pathlib import Path

from core.kernel import Kernel
from core.health import health
from core.plugins import plugin_manager
from core.service import service


VERSION = "0.1.0"
NAME = "DataVision X"


def start():
    if service.is_running():
        print("DataVision X already running")
        return

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "core.daemon"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    service.save_pid(process.pid)

    print("DataVision X started")
    print(f"PID: {process.pid}")


def stop():
    if service.stop():
        print("DataVision X stopped")
    else:
        print("DataVision X is not running")


def status():
    data = health.report()

    print("DataVision X Status")
    print("==============================")
    print(f"Status : {data['status']}")
    print(f"Process: {data['process']}")
    print(f"PID    : {data['pid']}")
    print(f"Uptime : {data['uptime']} sec")


def doctor():
    plugin_manager.load_plugins()

    data = health.report()

    print("DataVision X Doctor")
    print("==============================")
    print(f"Kernel  : OK")
    print(f"Runtime : {data['status']}")
    print(f"Process : {data['process']}")
    print(f"PID     : {data['pid']}")
    print(f"Plugins : {data['plugins']}")
    print(f"Health  : HEALTHY")


def version():
    print(NAME)
    print(f"Version : {VERSION}")


def plugins():
    plugin_manager.load_plugins()

    print("Loaded plugins")
    print("==============================")

    for item in plugin_manager.list_plugins():
        print(item)


def logs():
    log_file = Path("logs/datavisionx.log")

    if not log_file.exists():
        print("Log file not found")
        return

    print(
        log_file.read_text(
            encoding="utf-8"
        )[-2000:]
    )


def help_menu():
    print("""
DataVision X CLI

Commands:

start
stop
status
doctor
version
plugins
logs
help
""")


def main():
    if len(sys.argv) < 2:
        help_menu()
        return

    command = sys.argv[1]

    commands = {
        "start": start,
        "stop": stop,
        "status": status,
        "doctor": doctor,
        "version": version,
        "plugins": plugins,
        "logs": logs,
        "help": help_menu,
    }

    action = commands.get(command)

    if action:
        action()
    else:
        print("Unknown command")
        help_menu()


if __name__ == "__main__":
    main()
