from fastapi import HTTPException
from app.services.user import UserService
from app.dtos.user import UserDefaultDto


class UserHandler:
    def __init__(self):
        self.user_service = UserService()

    async def get_me(self, user_id: str) -> UserDefaultDto:
        user = await self.user_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserDefaultDto(**user.model_dump())
