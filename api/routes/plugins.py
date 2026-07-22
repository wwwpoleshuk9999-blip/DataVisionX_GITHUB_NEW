import os
import json
import zipfile
import shutil
from fastapi import APIRouter, Header, HTTPException, UploadFile, File

from auth.session import session_manager
from auth.users.service import user_service
from auth.permissions.roles import has_permission

from plugin_manager.manager import plugin_manager


router = APIRouter(
    prefix="/plugins",
    tags=["Plugins"]
)


UPLOAD_DIR = "uploads"
PLUGIN_DIR = "plugins"



def get_current_user(authorization: str):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    username = session_manager.get_user(token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = user_service.get(username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user



def admin_only(user):

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )



@router.get("")
def list_plugins(
    authorization: str = Header(None)
):

    user = get_current_user(
        authorization
    )

    plugins = plugin_manager.list_plugins()

    return {
        "count": len(plugins),
        "plugins": plugins
    }



@router.post("/install")
async def install_plugin(
    file: UploadFile = File(...),
    authorization: str = Header(None)
):

    user = get_current_user(
        authorization
    )

    admin_only(user)


    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )


    zip_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )


    with open(
        zip_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    extract_dir = os.path.join(
        UPLOAD_DIR,
        "extract"
    )


    if os.path.exists(extract_dir):

        shutil.rmtree(
            extract_dir
        )


    os.makedirs(
        extract_dir
    )


    try:

        with zipfile.ZipFile(
            zip_path,
            "r"
        ) as z:

            z.extractall(
                extract_dir
            )


    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid zip"
        )



    manifest_path = None


    for root, dirs, files in os.walk(
        extract_dir
    ):

        if "manifest.json" in files:

            manifest_path = os.path.join(
                root,
                "manifest.json"
            )

            break



    if not manifest_path:

        raise HTTPException(
            status_code=400,
            detail="manifest.json missing"
        )



    with open(
        manifest_path,
        "r",
        encoding="utf-8"
    ) as f:

        manifest = json.load(f)



    plugin_name = os.path.basename(
        os.path.dirname(
            manifest_path
        )
    )



    destination = os.path.join(
        PLUGIN_DIR,
        plugin_name
    )


    if os.path.exists(destination):

        shutil.rmtree(
            destination
        )


    shutil.copytree(
        os.path.dirname(manifest_path),
        destination
    )


    plugin_manager.scan_plugins()


    return {

        "message": "Plugin installed",

        "plugin": plugin_name,

        "version": manifest.get(
            "version"
        )
    }

