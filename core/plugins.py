import importlib
from pathlib import Path

from core.runtime import runtime
from core.logger import logger


class PluginManager:

    def __init__(self):
        self.plugins = {}

    def load_plugins(self):

        plugins_dir = Path("plugins")

        if not plugins_dir.exists():
            logger.warning(
                "Plugins directory not found."
            )
            return

        for file in plugins_dir.glob("*.py"):

            if file.name == "__init__.py":
                continue

            module_name = f"plugins.{file.stem}"

            if module_name in self.plugins:
                continue

            try:
                module = importlib.import_module(
                    module_name
                )

                if hasattr(module, "register"):
                    event_bus = runtime.get_service("event_bus")

                    if event_bus:
                        module.register(event_bus)

                info = getattr(
                    module,
                    "PLUGIN_INFO",
                    {}
                )

                self.plugins[module_name] = {
                    "module": module_name,
                    "name": info.get(
                        "name",
                        module_name
                    ),
                    "version": info.get(
                        "version",
                        "unknown"
                    ),
                    "description": info.get(
                        "description",
                        ""
                    ),
                    "status": "LOADED",
                }

                logger.info(
                    f"Plugin loaded: {module_name}"
                )

            except Exception as e:
                logger.error(
                    f"Failed to load {module_name}: {e}"
                )

    def list_plugins(self):
        return list(
            self.plugins.values()
        )

    def count(self):
        return len(
            self.plugins
        )


plugin_manager = PluginManager()
