from fastapi import APIRouter, Request

from core.runtime import runtime
from core.health import health
from core.events import add_event


router = APIRouter(
    prefix="/runtime",
    tags=["Runtime"]
)


@router.get("")
def runtime_status(
    request: Request
):
    return {
        "runtime": runtime.read(),
        "uptime": runtime.uptime()
    }


@router.get("/health")
def runtime_health(
    request: Request
):
    return {
        "health": health.report()
    }


@router.post("/reload")
def runtime_reload(
    request: Request
):

    runtime.reload()

    user = getattr(
        request.state,
        "user",
        {
            "username": "system"
        }
    )

    add_event(
        "RUNTIME_RELOAD",
        user=user.get(
            "username",
            "system"
        )
    )

    return {
        "status": "RELOADED",
        "runtime": runtime.read(),
        "user": user
    }
