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

    username = session_manager.get_user(token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = user_service.get(username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user



def find_plugin(name):

    plugins = plugin_manager.plugins

    if name in plugins:
        return name

    for key, data in plugins.items():

        if data.get("name") == name:
            return key

    return None



@router.post("/{name}/start")
def start_plugin(
    name: str,
    authorization: str = Header(None)
):

    get_current_user(authorization)

    plugin = find_plugin(name)

    if not plugin:
        raise HTTPException(
            status_code=404,
            detail="Plugin not found"
        )

    if not plugin_manager.start(plugin):
        raise HTTPException(
            status_code=400,
            detail="Failed to start plugin"
        )

    return {
        "plugin": plugin,
        "status": "RUNNING"
    }



@router.post("/{name}/stop")
def stop_plugin(
    name: str,
    authorization: str = Header(None)
):

    get_current_user(authorization)

    plugin = find_plugin(name)

    if not plugin:
        raise HTTPException(
            status_code=404,
            detail="Plugin not found"
        )

    plugin_manager.stop(plugin)

    return {
        "plugin": plugin,
        "status": "STOPPED"
    }



@router.post("/{name}/restart")
def restart_plugin(
    name: str,
    authorization: str = Header(None)
):

    get_current_user(authorization)

    plugin = find_plugin(name)

    if not plugin:
        raise HTTPException(
            status_code=404,
            detail="Plugin not found"
        )

    plugin_manager.stop(plugin)

    if not plugin_manager.start(plugin):
        raise HTTPException(
            status_code=400,
            detail="Restart failed"
        )

    return {
        "plugin": plugin,
        "status": "RUNNING"
    }



@router.get("/{name}/status")
def plugin_status(
    name: str,
    authorization: str = Header(None)
):

    get_current_user(authorization)

    plugin = find_plugin(name)

    if not plugin:
        raise HTTPException(
            status_code=404,
            detail="Plugin not found"
        )

    return {
        "id": plugin,
        **plugin_manager.plugins[plugin]
    }
