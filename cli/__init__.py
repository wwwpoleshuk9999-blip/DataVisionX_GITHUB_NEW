import sys

from core.kernel import Kernel
from core.health import health


kernel = Kernel()


def start():
    kernel.start()


def stop():
    kernel.stop()


def status():
    print("DataVision X Status")
    print("=" * 30)
    print(health.report())


def doctor():
    report = health.report()

    print("DataVision X Health")
    print("=" * 30)
    print(f"Status : {report['status']}")
    print(f"Uptime : {report['uptime']} sec")

    if report["status"] == "RUNNING":
        print("System : HEALTHY")
    else:
        print("System : STOPPED")


def main():
    if len(sys.argv) < 2:
        print("Usage: dvx <command>")
        print("Commands: start, stop, status, doctor")
        return

    command = sys.argv[1]

    commands = {
        "start": start,
        "stop": stop,
        "status": status,
        "doctor": doctor,
    }

    action = commands.get(command)

    if action:
        action()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
