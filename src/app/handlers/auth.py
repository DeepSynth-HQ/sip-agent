from app.services.auth import AuthService
from app.dtos.auth import AuthResponseDto, LoginResponseDto
import secrets
from app.database.redis import RedisService
from settings import config
from fastapi.responses import RedirectResponse
from fastapi import Request, HTTPException
from app.core.errors import Error, ERROR_DETAILS
from settings import logger


class AuthHandler:
    def __init__(self):
        self.auth_service = AuthService()
        self.redis_service = RedisService(config.REDIS_URI)

    async def handle_google_login(self, request: Request):
        """Initiate Google OAuth2 flow"""
        # Generate state token to prevent CSRF
        state = secrets.token_urlsafe(32)
        self.redis_service.get_client().set(state, "true")

        # Construct Google OAuth URL
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={config.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={config.GOOGLE_REDIRECT_URI}"
            "&scope=openid%20email%20profile"
            f"&state={state}"
        )
        response = RedirectResponse(url=google_auth_url)
        return response

    async def handle_google_callback(
        self, code: str, state: str, request: Request
    ) -> RedirectResponse:
        try:
            redirect_url = await self.auth_service.handle_google_callback(
                code, state, request
            )
            return RedirectResponse(url=redirect_url)
        except Exception as e:
            logger.error(f"Error handling Google callback: {str(e)}")
            fallback_url = config.FRONTEND_URL + "?error=" + str(e)
            return RedirectResponse(url=fallback_url)

    async def login_google(self, access_token: str) -> LoginResponseDto:
        try:
            return await self.auth_service.login_google(access_token)
        except Exception as e:
            raise HTTPException(
                status_code=ERROR_DETAILS[Error.INTERNAL_SERVER_ERROR],
                detail=str(e),
            )
