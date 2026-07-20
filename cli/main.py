import sys
import subprocess
from pathlib import Path

from core.health import health
from core.plugins import plugin_manager
from core.service import service
from core.config import config


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
    print("Kernel  : OK")
    print(f"Runtime : {data['status']}")
    print(f"Process : {data['process']}")
    print(f"PID     : {data['pid']}")
    print(f"Plugins : {data['plugins']}")
    print("Health  : HEALTHY")


def version():
    print(
        config.get(
            "app",
            "name",
            default="DataVision X"
        )
    )

    print(
        "Version :",
        config.get(
            "app",
            "version",
            default="unknown"
        )
    )


def plugins():
    plugin_manager.load_plugins()

    print("DataVision X Plugins")
    print("==============================")

    plugins_list = plugin_manager.list_plugins()

    if not plugins_list:
        print("No plugins loaded")
        return

    for plugin in plugins_list:
        print()
        print(f"Name   : {plugin['name']}")
        print(f"Version: {plugin['version']}")
        print(f"Status : {plugin['status']}")
        print(f"Info   : {plugin['description']}")


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


def config_show():
    print("DataVision X Config")
    print("==============================")

    for section, values in config.all().items():

        print(f"\n[{section}]")

        if isinstance(values, dict):
            for key, value in values.items():
                print(f"{key}: {value}")


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
config
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
        "config": config_show,
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
