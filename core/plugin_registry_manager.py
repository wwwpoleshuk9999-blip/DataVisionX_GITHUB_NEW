from core.plugin_registry import (
    register_plugin,
    get_registry,
    save_registry,
    load_registry
)


class PluginRegistryManager:

    def __init__(self):
        pass


    def register(
        self,
        plugin_id,
        name,
        version,
        path
    ):
        return register_plugin(
            plugin_id,
            name,
            version,
            path
        )


    def list_plugins(self):
        return get_registry()


    def get_plugin(self, plugin_id):

        registry = load_registry()

        for plugin in registry:

            if plugin["id"] == plugin_id:
                return plugin

        return None


    def update_status(
        self,
        plugin_id,
        status
    ):

        registry = load_registry()

        for plugin in registry:

            if plugin["id"] == plugin_id:

                plugin["status"] = status

                save_registry(
                    registry
                )

                return plugin

        return None


    def remove(
        self,
        plugin_id
    ):

        registry = load_registry()

        new_registry = [
            plugin
            for plugin in registry
            if plugin["id"] != plugin_id
        ]

        save_registry(
            new_registry
        )

        return True
