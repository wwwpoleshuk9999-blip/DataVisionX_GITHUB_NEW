from fastapi import APIRouter

from services.system_service import system_service


router = APIRouter()


@router.get("/system")
def system():
    return system_service.info()
