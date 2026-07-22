from fastapi import APIRouter, HTTPException, Header

from auth.users.service import user_service
from auth.session import session_manager

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


def get_token(authorization: str):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header"
        )

    return authorization.replace("Bearer ", "")


@router.post("/login")
def login(username: str, password: str):
    user = user_service.login(username, password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = session_manager.create(user.username)

    return {
        "token": token,
        "user": user.to_dict(),
        "message": "Login successful"
    }


@router.post("/logout")
def logout(authorization: str = Header(None)):

    token = get_token(authorization)

    if not session_manager.get_user(token):
        raise HTTPException(
            status_code=401,
            detail="Invalid session token"
        )

    session_manager.delete(token)

    return {
        "message": "Logout successful"
    }


@router.get("/me")
def me(authorization: str = Header(None)):

    token = get_token(authorization)

    username = session_manager.get_user(token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid session token"
        )

    user = user_service.get(username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user.to_dict()
