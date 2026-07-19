from core.events import event_bus
from core.kernel import Kernel
from core.health import health


def on_kernel_started(data):
    print("=" * 50)
    print("EVENT RECEIVED")
    print(f"Kernel : {data['name']}")
    print(f"Version: {data['version']}")
    print("=" * 50)


def on_kernel_stopped(data):
    print("=" * 50)
    print("EVENT RECEIVED")
    print("Kernel stopped")
    print("=" * 50)


event_bus.subscribe("kernel.started", on_kernel_started)
event_bus.subscribe("kernel.stopped", on_kernel_stopped)


kernel = Kernel()

kernel.start()

print("=" * 50)
print("HEALTH REPORT")
print(health.report())
print("=" * 50)

kernel.stop()
