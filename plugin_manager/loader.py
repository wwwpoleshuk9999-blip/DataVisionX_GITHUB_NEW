import json
from pathlib import Path

from plugin_manager.models import PluginInfo


class PluginLoader:

    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = Path(plugins_dir)

    def discover(self):
        plugins = []

        if not self.plugins_dir.exists():
            return plugins

        for folder in self.plugins_dir.iterdir():

            if not folder.is_dir():
                continue

            manifest = folder / "manifest.json"

            if not manifest.exists():
                continue

            try:

                with open(
                    manifest,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

                plugins.append(

                    PluginInfo(

                        id=data.get("id", folder.name),

                        name=data.get("name", folder.name),

                        version=data.get("version", "0.0.0"),

                        author=data.get("author", "Unknown"),

                        description=data.get("description", ""),

                        api_version=data.get("api_version", "1.0"),

                        path=str(folder),

                        permissions=data.get("permissions", {}),

                        dependencies=data.get("dependencies", [])

                    )

                )

            except Exception as e:

                print(
                    f"Loader error: {folder.name}: {e}"
                )

        return plugins
