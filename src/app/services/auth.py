from settings.config import config
from typing import Dict
import aiohttp
from google.oauth2 import id_token
from google.auth.transport import requests
from utils.jwt import create_jwt_token, verify_jwt_token
from datetime import datetime, timezone, timedelta
from app.dtos.auth import AuthResponseDto, LoginResponseDto
from app.dtos.user import UserDefaultDto
from fastapi import Request, HTTPException
from app.database.redis import RedisService


class AuthService:
    def __init__(self):
        self.google_client_id = config.GOOGLE_CLIENT_ID
        self.google_client_secret = config.GOOGLE_CLIENT_SECRET
        self.google_redirect_uri = config.GOOGLE_REDIRECT_URI
        self.redis_service = RedisService()

    async def _handle_google_callback(self, code: str) -> AuthResponseDto:
        """Handle the OAuth2 callback from Google"""
        try:
            # Exchange authorization code for tokens
            token_url = "https://oauth2.googleapis.com/token"
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    token_url,
                    data={
                        "client_id": self.google_client_id,
                        "client_secret": self.google_client_secret,
                        "code": code,
                        "redirect_uri": self.google_redirect_uri,
                        "grant_type": "authorization_code",
                    },
                ) as response:
                    token_data = await response.json()

            if "error" in token_data:
                raise ValueError(f"Error getting tokens: {token_data['error']}")

            # Verify ID token
            idinfo = id_token.verify_oauth2_token(
                token_data["id_token"], requests.Request(), self.google_client_id
            )

            # Get user info
            user_id = idinfo["sub"]  # Standard JWT uses 'sub' for subject/user ID
            email = idinfo.get("email")
            name = idinfo.get("name")
            picture = idinfo.get("picture")

            # Create JWT token with standard claims
            access_token = create_jwt_token(
                {
                    "sub": user_id,  # Subject (user ID)
                    "iss": "https://accounts.google.com",
                    "iat": datetime.now(timezone.utc),
                    "exp": datetime.now(timezone.utc) + timedelta(days=30),
                    "email": email,
                    "name": name,
                    "picture": picture,
                    "token_type": "access_token",
                }
            )

            refresh_token = create_jwt_token(
                {
                    "sub": user_id,
                    "iat": datetime.now(timezone.utc),
                    "exp": datetime.now(timezone.utc) + timedelta(days=365),
                    "token_type": "refresh_token",
                }
            )

            return AuthResponseDto(
                access_token=access_token,
                refresh_token=refresh_token,
            )

        except Exception as e:
            raise ValueError(f"Failed to process Google callback: {str(e)}")

    async def handle_google_callback(
        self, code: str, state: str, request: Request
    ) -> str:
        """Handle the OAuth2 callback from Google"""
        # Verify state token
        state_data = self.redis_service.get_client().get(state)
        if state_data is None:
            raise HTTPException(status_code=400, detail="Invalid state parameter")

        # Delete state token after verification
        self.redis_service.get_client().delete(state)

        try:
            result = await self._handle_google_callback(code)
            frontend_url = (
                config.FRONTEND_URL
                + "?token="
                + result.access_token
                + "&refresh_token="
                + result.refresh_token
            )
            return frontend_url

        except Exception as e:
            raise ValueError(f"Failed to process Google callback: {str(e)}")

    async def login_google(self, token: str) -> LoginResponseDto:
        """Handle direct Google token login"""
        try:
            user_data = verify_jwt_token(token)

            user = UserDefaultDto(
                id=user_data["sub"],
                email=user_data["email"],
                name=user_data["name"],
                picture=user_data["picture"],
            )

            return LoginResponseDto(
                user=user,
            )

        except ValueError as e:
            raise ValueError(f"Invalid Google token: {str(e)}")
