from core.event_bus import event_bus
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

    event_bus.publish(
        action,
        {
            "action": action,
            "plugin": plugin,
            "user": user
        }
    )

    return result



def get_events():

    return load_events()
