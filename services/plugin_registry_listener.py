from core.runtime import runtime


def plugin_registry_listener(data):

    if not data:
        return

    plugin_id = data.get("plugin")
    status = data.get("status")

    if not plugin_id or not status:
        return

    manager = runtime.plugin_registry

    result = manager.update_status(
        plugin_id,
        status
    )

    if result:
        print(
            f"PLUGIN REGISTRY UPDATED: {plugin_id} -> {status}"
        )
