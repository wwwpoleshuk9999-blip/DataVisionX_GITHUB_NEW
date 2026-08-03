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




@router.post("/start")
def runtime_start(request: Request):
    data = runtime.start()
    user = getattr(request.state, "user", {"username": "system"})
    add_event("RUNTIME_START", user=user.get("username", "system"))
    return {"status": "RUNNING", "runtime": data, "user": user}


@router.post("/stop")
def runtime_stop(request: Request):
    data = runtime.stop()
    user = getattr(request.state, "user", {"username": "system"})
    add_event("RUNTIME_STOP", user=user.get("username", "system"))
    return {"status": "STOPPED", "runtime": data, "user": user}


@router.post("/restart")
def runtime_restart(request: Request):
    data = runtime.restart()
    user = getattr(request.state, "user", {"username": "system"})
    add_event("RUNTIME_RESTART", user=user.get("username", "system"))
    return {"status": "RESTARTED", "runtime": data, "user": user}


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
