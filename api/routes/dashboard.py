from fastapi import APIRouter
from services.dashboard_service import dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard_info():
    return dashboard()
