from core.logger import logger
from core.config import config
from core.events import event_bus
from core.plugins import plugin_manager
from core.health import health


class Kernel:
    def __init__(self):
        self.running = False
        self.name = config.get("app", "name", default="DataVision X")
        self.version = config.get("app", "version", default="0.0.0")

    def start(self):
        self.running = True

        health.start()

        logger.info(f"{self.name} {self.version}")
        logger.info("Kernel started.")

        plugin_manager.load_plugins()

        event_bus.publish(
            "kernel.started",
            {
                "name": self.name,
                "version": self.version
            }
        )

    def stop(self):
        self.running = False

        health.stop()

        logger.info("Kernel stopped.")

        event_bus.publish(
            "kernel.stopped",
            {
                "name": self.name,
                "version": self.version
            }
        )
