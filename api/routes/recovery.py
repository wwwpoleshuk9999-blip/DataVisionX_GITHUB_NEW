from fastapi import APIRouter

from core.recovery import recovery


router = APIRouter(
    prefix="/recovery",
    tags=["Recovery"]
)


@router.get("/status")
def recovery_status():

    return {
        "recovery": recovery.check_and_recover()
    }


@router.get("/info")
def recovery_info():

    return {
        "status": recovery.status()
    }


@router.get("/history")
def recovery_history():

    return {
        "events": recovery.get_history()
    }


@router.post("/run")
def recovery_run():

    return {
        "recovery": recovery.check_and_recover()
    }
