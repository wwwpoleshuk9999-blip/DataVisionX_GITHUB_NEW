from fastapi import APIRouter, HTTPException
from auth.users.service import user_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(username: str, password: str):
    user = user_service.login(username, password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "user": user.to_dict(),
        "message": "Login successful"
    }


@router.get("/me")
def me(username: str):
    user = user_service.get(username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user.to_dict()
