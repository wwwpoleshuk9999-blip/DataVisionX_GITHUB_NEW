from core.runtime import runtime

from plugin_manager.permissions import PermissionManager
from plugin_manager.event_bus import EventBus
from plugin_manager.storage import PluginStorage
from plugin_manager.manager import plugin_manager
from services.websocket_bridge import websocket_event_listener
from services.plugin_registry_listener import plugin_registry_listener
from ai.service import AIService


def register_core_services():

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


    if not runtime.registry.exists("event_bus"):

        runtime.register_service(
            "event_bus",
            EventBus(
                permissions
            )
        )


    if not runtime.registry.exists("storage"):

        runtime.register_service(
            "storage",
            PluginStorage(
                permissions
            )
        )





    if not runtime.registry.exists("plugin_manager"):

        runtime.register_service(
            "plugin_manager",
            plugin_manager
        )

    if not runtime.registry.exists("ai_service"):

        runtime.register_service(
            "ai_service",
            AIService()
        )

    event_bus = runtime.get_service(
        "event_bus"
    )

    if event_bus:

        event_bus.register(
            "system",
            "plugin_started",
            websocket_event_listener
        )

        event_bus.register(
            "system",
            "plugin_stopped",
            websocket_event_listener
        )

        event_bus.register(
            "system",
            "plugin_started",
            plugin_registry_listener
        )

        event_bus.register(
            "system",
            "plugin_stopped",
            plugin_registry_listener
        )

        event_bus.register(
            "system",
            "ai_chat_completed",
            websocket_event_listener
        )

    return runtime.registry.list_services()



services = register_core_services()
