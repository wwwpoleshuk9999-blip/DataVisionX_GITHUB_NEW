import shutil
from pathlib import Path


class PluginInstaller:

    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = Path(plugins_dir)

    def install(self, source):

        source = Path(source)

        if not source.exists():
            return False, "Source not found"

        destination = self.plugins_dir / source.name

        if destination.exists():
            return False, "Plugin already installed"

        shutil.copytree(
            source,
            destination
        )

        return True, str(destination)
