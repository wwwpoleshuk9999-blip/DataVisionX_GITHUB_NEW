from fastapi import APIRouter

from core.watchdog import watchdog


router = APIRouter(
    prefix="/watchdog",
    tags=["Watchdog"]
)


@router.get("/status")
def watchdog_status():
    return {
        "watchdog": watchdog.check()
    }


@router.get("/info")
def watchdog_info():
    return {
        "watchdog": watchdog.status_info()
    }


@router.get("/history")
def watchdog_history():
    return {
        "events": watchdog.get_history()
    }
