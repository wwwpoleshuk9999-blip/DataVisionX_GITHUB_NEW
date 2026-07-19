from core.events import event_bus
from core.kernel import Kernel


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
kernel.stop()
