from fastapi import APIRouter

from services.health_service import health_service


router = APIRouter()


@router.get("/health")
def health():
    return health_service.report()
