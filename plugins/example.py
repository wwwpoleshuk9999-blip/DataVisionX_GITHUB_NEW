from core.logger import logger


def register(event_bus):
    logger.info("Example plugin loaded.")

    def on_started(data):
        logger.info(
            f"Plugin received start event: {data['name']} {data['version']}"
        )

    event_bus.subscribe("kernel.started", on_started)
