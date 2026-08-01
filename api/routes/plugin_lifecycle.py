from fastapi import APIRouter, Header, HTTPException
from core.runtime import runtime

from auth.session import session_manager
from auth.users.service import user_service

from plugin_manager.manager import plugin_manager

from core.events import add_event


router = APIRouter(
    prefix="/plugins",
    tags=["Plugin Lifecycle"]
)


def get_current_user(authorization: str):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )


    token = authorization.replace(
        "Bearer ",
        ""
    )


    username = session_manager.get_user(
        token
    )


    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    user = user_service.get(
        username
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user



@router.get("/{plugin_id}/status")
def plugin_status(
    plugin_id: str,
    authorization: str = Header(None)
):

    get_current_user(
        authorization
    )

    plugin_manager.discover()


    plugin = plugin_manager.plugins.get(
        plugin_id
    )


    if not plugin:
        raise HTTPException(
            status_code=404,
            detail="Plugin not found"
        )


    return {
        "id": plugin.id,
        "name": plugin.name,
        "version": plugin.version,
        "description": plugin.description,
        "status": plugin.status
    }



@router.post("/{plugin_id}/start")
def start_plugin(
    plugin_id: str,
    authorization: str = Header(None)
):

    user = get_current_user(
        authorization
    )


    plugin_manager.discover()


    result = plugin_manager.start(
        plugin_id
    )


    if result:

        add_event(
            "START",
            plugin_id,
            user.username
        )

        return {
            "plugin": plugin_id,
            "status": "RUNNING"
        }


    raise HTTPException(
        status_code=400,
        detail="Failed to start plugin"
    )



@router.post("/{plugin_id}/stop")
def stop_plugin(
    plugin_id: str,
    authorization: str = Header(None)
):

    user = get_current_user(
        authorization
    )


    result = plugin_manager.stop(
        plugin_id
    )


    if result:

        add_event(
            "STOP",
            plugin_id,
            user.username
        )

        return {
            "plugin": plugin_id,
            "status": "STOPPED"
        }


    raise HTTPException(
        status_code=400,
        detail="Failed to stop plugin"
    )



@router.post("/{plugin_id}/restart")
def restart_plugin(
    plugin_id: str,
    authorization: str = Header(None)
):

    user = get_current_user(
        authorization
    )


    plugin_manager.discover()


    result = plugin_manager.restart(
        plugin_id
    )


    if result:

        add_event(
            "RESTART",
            plugin_id,
            user.username
        )

        return {
            "plugin": plugin_id,
            "status": "RUNNING"
        }


    raise HTTPException(
        status_code=400,
        detail="Failed to restart plugin"
    )
