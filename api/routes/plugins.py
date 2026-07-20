from fastapi import APIRouter

from services.plugin_service import plugin_service


router = APIRouter()


@router.get("/plugins")
def plugins():
    plugin_service.load()

    return {
        "count": plugin_service.count(),
        "plugins": plugin_service.list()
    }
