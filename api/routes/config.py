from fastapi import APIRouter

from services.config_service import config_service


router = APIRouter()


@router.get("/config")
def config():
    return config_service.all()
