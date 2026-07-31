from fastapi import APIRouter
from core.runtime import runtime

router = APIRouter(
    prefix="/health/plugins",
    tags=["Plugin Health"]
)


@router.get("")
def plugin_health():

    pm = runtime.get_service(
        "plugin_manager"
    )

    return {
        "plugins": pm.health.all()
    }


@router.get("/{plugin_id}")
def plugin_health_one(plugin_id: str):

    pm = runtime.get_service(
        "plugin_manager"
    )

    return pm.health.get(
        plugin_id
    )
