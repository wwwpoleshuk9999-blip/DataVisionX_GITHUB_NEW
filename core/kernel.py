from core.logger import logger
from core.config import config
from core.events import event_bus
from core.plugins import plugin_manager


class Kernel:
    def __init__(self):
        self.running = False
        self.name = config.get("app", "name", default="DataVision X")
        self.version = config.get("app", "version", default="0.0.0")

    def start(self):
        self.running = True

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

        logger.info("Kernel stopped.")

        event_bus.publish(
            "kernel.stopped",
            {
                "name": self.name,
                "version": self.version
            }
        )
