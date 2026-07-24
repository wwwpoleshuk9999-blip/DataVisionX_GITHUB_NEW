from fastapi import APIRouter

from core.events import get_events


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("")
def list_events():

    return {
        "events": get_events()
    }
