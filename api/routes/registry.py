from fastapi import APIRouter, Header, HTTPException

from core.plugin_registry import get_registry

from auth.session import session_manager
from auth.users.service import user_service


router = APIRouter(
    prefix="/registry",
    tags=["Plugin Registry"]
)


def check_user(authorization: str):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )


    token = authorization.replace(
        "Bearer ",
        ""
    )


    username = session_manager.get_user(
        token
    )


    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    user = user_service.get(
        username
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user



@router.get("")
def registry(
    authorization: str = Header(None)
):

    check_user(
        authorization
    )


    return {

        "registry":
        get_registry()

    }
