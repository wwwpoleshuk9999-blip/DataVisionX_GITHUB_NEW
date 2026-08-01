from core.event_store import (
    save_event,
    get_events as load_events
)


def add_event(
    action,
    plugin=None,
    user="system"
):

    result = save_event(
        action,
        plugin,
        user
    )

    return result


def get_events():
    return load_events()
