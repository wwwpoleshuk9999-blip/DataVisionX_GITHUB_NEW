from fastapi import Request, HTTPException

PUBLIC_PATHS = [
    "/",
    "/health",
    "/system",
    "/plugins",
    "/dashboard",
    "/dashboard/status",

    "/auth/login",

    "/docs",
    "/docs/",
    "/openapi.json",
    "/redoc",

    "/favicon.ico"
]


async def auth_middleware(request: Request, call_next):
    path = request.url.path

    # Разрешаем все статические файлы Dashboard
    if path.startswith("/web"):
        return await call_next(request)

    # Разрешаем публичные маршруты
    if path in PUBLIC_PATHS:
        return await call_next(request)

    # Проверяем авторизацию
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    return await call_next(request)
