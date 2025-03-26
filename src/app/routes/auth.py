from fastapi import APIRouter, Request
from app.handlers.auth import AuthHandler

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login/google")
async def google_login(request: Request):
    auth_handler = AuthHandler()
    return await auth_handler.handle_google_login(request)


@router.get("/callback/google", include_in_schema=False)
async def google_callback(code: str, state: str, request: Request):
    auth_handler = AuthHandler()
    return await auth_handler.handle_google_callback(code, state, request)
