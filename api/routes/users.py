from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from auth.session import session_manager
from auth.users.service import user_service
from auth.permissions.roles import has_permission


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "viewer"


class RoleUpdate(BaseModel):
    role: str


class PasswordUpdate(BaseModel):
    password: str



def get_current_user(authorization: str):

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


    token = authorization.replace(
        "Bearer ",
        ""
    )


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


    return user



def check_permission(user, action):

    if not has_permission(
        user.role,
        "users",
        action
    ):

        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )



@router.get("")
def list_users(
    authorization: str = Header(None)
):

    current_user = get_current_user(
        authorization
    )


    check_permission(
        current_user,
        "read"
    )


    users = []


    for username in user_service.users:

        user = user_service.get(username)

        users.append(
            user.to_dict()
        )


    return {
        "count": len(users),
        "users": users
    }



@router.post("")
def create_user(
    data: UserCreate,
    authorization: str = Header(None)
):

    current_user = get_current_user(
        authorization
    )


    check_permission(
        current_user,
        "create"
    )


    if user_service.get(data.username):

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )


    user = user_service.create(
        data.username,
        data.password,
        data.role
    )


    return {
        "message": "User created",
        "user": user.to_dict()
    }



@router.delete("/{username}")
def delete_user(
    username: str,
    authorization: str = Header(None)
):

    current_user = get_current_user(
        authorization
    )


    check_permission(
        current_user,
        "delete"
    )


    if username == "admin":

        raise HTTPException(
            status_code=400,
            detail="Cannot delete admin"
        )


    if not user_service.get(username):

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    del user_service.users[username]

    user_service.save()


    return {
        "message": "User deleted",
        "username": username
    }



@router.put("/{username}/role")
def update_role(
    username: str,
    data: RoleUpdate,
    authorization: str = Header(None)
):

    current_user = get_current_user(
        authorization
    )


    check_permission(
        current_user,
        "update"
    )


    user = user_service.get(username)


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    user.role = data.role

    user_service.save()


    return {
        "message": "Role updated",
        "user": user.to_dict()
    }



@router.put("/{username}/password")
def update_password(
    username: str,
    data: PasswordUpdate,
    authorization: str = Header(None)
):

    current_user = get_current_user(
        authorization
    )


    check_permission(
        current_user,
        "update"
    )


    user = user_service.get(username)


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    user.password = user_service.hash_password(
        data.password
    )

    user_service.save()


    return {
        "message": "Password updated",
        "username": username
    }
