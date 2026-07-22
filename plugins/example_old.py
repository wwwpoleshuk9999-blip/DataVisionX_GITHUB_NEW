from core.logger import logger


PLUGIN_INFO = {
    "name": "Example Plugin",
    "version": "0.1.0",
    "description": "Example DataVision X plugin",
}


def register(event_bus):

    logger.info(
        f"{PLUGIN_INFO['name']} loaded"
    )

    def on_started(data):
        logger.info(
            f"Plugin received start event: "
            f"{data['name']} {data['version']}"
        )

    event_bus.subscribe(
        "kernel.started",
        on_started
    )
