import jwt
from datetime import datetime, timedelta
from typing import Dict
from settings import config


def create_jwt_token(payload: Dict, expires_in: int = 30) -> str:
    """Create a JWT token with the given payload"""
    expiration = datetime.now() + timedelta(days=expires_in)  # Token expires in 30 days
    payload["exp"] = expiration

    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm="HS256")


def verify_jwt_token(token: str) -> Dict:
    """Verify and decode a JWT token"""
    try:
        print("TOKEN", token)
        return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
