from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str
    email: Optional[str] = None
    name: str
    picture: str
    username: Optional[str] = None
    google_id: Optional[str] = None
