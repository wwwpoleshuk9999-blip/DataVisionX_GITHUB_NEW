from core.logger import logger
from core.config import config

class Kernel:
    def __init__(self):
        self.running = False
        self.name = config.get("app", "name", default="DataVision X")
        self.version = config.get("app", "version", default="0.0.0")

    def start(self):
        self.running = True
        logger.info(f"{self.name} {self.version}")
        logger.info("Kernel started.")

    def stop(self):
        self.running = False
        logger.info("Kernel stopped.")
