from fastapi import APIRouter

from core.recovery import recovery

router = APIRouter(
    prefix="/recovery",
    tags=["Recovery"]
)

@router.post("/test")
def recovery_test():

    recovery.write_event("FAILURE_SIMULATED")
    recovery.write_event("RECOVERY_STARTED")
    recovery.write_event("RECOVERY_SUCCESS")

    return {
        "message": "Recovery test completed",
        "status": "OK"
    }
