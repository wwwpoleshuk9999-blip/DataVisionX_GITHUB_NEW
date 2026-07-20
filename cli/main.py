import sys
import subprocess
from pathlib import Path

from services.health_service import health_service
from services.plugin_service import plugin_service
from services.config_service import config_service
from services.system_service import system_service

from core.service import service


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
    data = health_service.report()

    print("DataVision X Status")
    print("==============================")
    print(f"Status : {data['status']}")
    print(f"Process: {data['process']}")
    print(f"PID    : {data['pid']}")
    print(f"Uptime : {data['uptime']} sec")


def doctor():
    plugin_service.load()

    data = health_service.report()

    print("DataVision X Doctor")
    print("==============================")
    print("Kernel  : OK")
    print(f"Runtime : {data['status']}")
    print(f"Process : {data['process']}")
    print(f"PID     : {data['pid']}")
    print(f"Plugins : {plugin_service.count()}")
    print("Health  : HEALTHY")


def version():
    print(system_service.name())
    print(
        "Version :",
        system_service.version()
    )


def plugins():
    plugin_service.load()

    print("DataVision X Plugins")
    print("==============================")

    for plugin in plugin_service.list():
        print(f"Name   : {plugin['name']}")
        print(f"Version: {plugin['version']}")
        print(f"Status : {plugin['status']}")
        print(f"Info   : {plugin['description']}")
        print()


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

    for section, values in config_service.all().items():
        print(f"\n[{section}]")

        if isinstance(values, dict):
            for key, value in values.items():
                print(f"{key}: {value}")


def system():
    print("DataVision X System")
    print("==============================")

    for key, value in system_service.info().items():
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
system
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
        "system": system,
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
