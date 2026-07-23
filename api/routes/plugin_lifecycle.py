from fastapi import APIRouter, Header, HTTPException

from auth.session import session_manager
from auth.users.service import user_service

from plugin_manager.manager import plugin_manager


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

    plugins = plugin_manager.plugins

    if plugin_id not in plugins:
        raise HTTPException(
            status_code=404,
            detail="Plugin not found"
        )

    data = plugins[plugin_id]

    return {
        "id": plugin_id,
        "name": data["name"],
        "version": data["version"],
        "description": data["description"],
        "status": data["status"]
    }



@router.get("/{plugin_id}/permissions")
def plugin_permissions(
    plugin_id: str,
    authorization: str = Header(None)
):

    get_current_user(
        authorization
    )

    if plugin_id not in plugin_manager.plugins:
        raise HTTPException(
            status_code=404,
            detail="Plugin not found"
        )


    return {
        "plugin": plugin_id,
        "permissions": plugin_manager.plugins[plugin_id].get(
            "permissions",
            {}
        )
    }



@router.post("/{plugin_id}/start")
def start_plugin(
    plugin_id: str,
    authorization: str = Header(None)
):

    get_current_user(
        authorization
    )

    if plugin_manager.start(
        plugin_id
    ):

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

    get_current_user(
        authorization
    )

    if plugin_manager.stop(
        plugin_id
    ):

        return {
            "plugin": plugin_id,
            "status": "STOPPED"
        }


    raise HTTPException(
        status_code=400,
        detail="Failed to stop plugin"
    )
