from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.middlewares.auth import get_current_user
from app.handlers.user import UserHandler

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    user_handler = UserHandler()
    return await user_handler.get_me(user.id)
