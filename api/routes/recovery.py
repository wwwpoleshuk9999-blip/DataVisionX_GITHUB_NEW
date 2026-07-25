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
