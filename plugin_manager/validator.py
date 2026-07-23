from pathlib import Path

from plugin_manager.models import PluginInfo


class PluginValidator:

    def validate(self, plugin: PluginInfo):

        errors = []

        if not plugin.id:
            errors.append("Missing plugin id")

        if not plugin.name:
            errors.append("Missing plugin name")

        if not plugin.version:
            errors.append("Missing version")

        if not plugin.api_version:
            errors.append("Missing api_version")

        if not isinstance(plugin.permissions, dict):
            errors.append("permissions must be dict")

        if not isinstance(plugin.dependencies, list):
            errors.append("dependencies must be list")

        if not Path(plugin.path).exists():
            errors.append("Plugin path does not exist")

        return len(errors) == 0, errors
