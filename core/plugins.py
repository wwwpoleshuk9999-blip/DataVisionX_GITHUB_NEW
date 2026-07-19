import importlib
from pathlib import Path

from core.events import event_bus
from core.logger import logger


class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        plugins_dir = Path("plugins")

        if not plugins_dir.exists():
            logger.warning("Plugins directory not found.")
            return

        for file in plugins_dir.glob("*.py"):

            if file.name == "__init__.py":
                continue

            module_name = f"plugins.{file.stem}"

            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "register"):
                    module.register(event_bus)

                self.plugins.append(module_name)

                logger.info(f"Plugin loaded: {module_name}")

            except Exception as e:
                logger.error(f"Failed to load {module_name}: {e}")


plugin_manager = PluginManager()
