from app.models.user import User
from app.database.mongo import get_collection


class UserService:
    def __init__(self):
        self.collection = get_collection("users")

    async def get_user(self, user_id: str) -> User | None:
        user = self.collection.find_one({"id": user_id})
        return User(**user) if user else None

    async def create_user(self, user: User) -> User:
        self.collection.insert_one(user.model_dump())
        return user

    async def update_user(self, user: User) -> User:
        self.collection.update_one({"id": user.id}, {"$set": user.model_dump()})
        return user

    async def delete_user(self, user_id: str) -> None:
        self.collection.delete_one({"id": user_id})

    async def get_user_by_google_id(self, google_id: str) -> User | None:
        user = self.collection.find_one({"google_id": google_id})
        return User(**user) if user else None
