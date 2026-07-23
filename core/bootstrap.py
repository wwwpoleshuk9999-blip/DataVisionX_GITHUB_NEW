from core.runtime import runtime

from plugin_manager.permissions import PermissionManager
from plugin_manager.event_bus import EventBus
from plugin_manager.storage import PluginStorage


def register_core_services():

    # 1. Permissions

    if not runtime.registry.exists("permissions"):

        permission_manager = PermissionManager(
            runtime
        )

        runtime.register_service(
            "permissions",
            permission_manager
        )


    permissions = runtime.get_service(
        "permissions"
    )


    # 2. Event Bus

    if not runtime.registry.exists("event_bus"):

        runtime.register_service(
            "event_bus",
            EventBus(
                permissions
            )
        )


    # 3. Storage

    if not runtime.registry.exists("storage"):

        runtime.register_service(
            "storage",
            PluginStorage(
                permissions
            )
        )


    return runtime.registry.list_services()



services = register_core_services()
