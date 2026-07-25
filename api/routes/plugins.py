from fastapi import APIRouter

from plugin_manager.manager import plugin_manager


router = APIRouter()


@router.get("/plugins")
def get_plugins():

    plugins = plugin_manager.discover()

    result = []

    for plugin in plugins:

        result.append(
            {
                "id": plugin.id,
                "name": plugin.name,
                "version": plugin.version,
                "status": getattr(plugin, "status", "STOPPED")
            }
        )

    return {
        "plugins": result
    }
