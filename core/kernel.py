from core.logger import logger
from core.runtime import runtime


class Kernel:
    VERSION = "0.1.0 Core Architecture"

    def __init__(self):
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True
        runtime.start()

        logger.info(f"DataVision X {self.VERSION}")
        logger.info("Kernel started.")

    def stop(self):
        if not self.running:
            return

        self.running = False
        runtime.stop()

        logger.info("Kernel stopped.")
