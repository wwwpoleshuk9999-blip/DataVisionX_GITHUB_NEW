from core.logger import logger
from core.runtime import runtime
from core.config import config


class Kernel:

    def __init__(self):
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True

        runtime.start()

        name = config.get(
            "app",
            "name",
            default="DataVision X"
        )

        version = config.get(
            "app",
            "version",
            default="unknown"
        )

        logger.info(
            f"{name} {version}"
        )

        logger.info(
            "Kernel started."
        )

    def stop(self):
        if not self.running:
            return

        self.running = False

        runtime.stop()

        logger.info(
            "Kernel stopped."
        )
