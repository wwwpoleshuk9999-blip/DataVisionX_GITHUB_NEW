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
