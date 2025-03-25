from pydantic import BaseModel
from typing import Optional


class AgentChatRequest(BaseModel):
    message: str
    images: list[str] = []
    stream: Optional[bool] = True
    user_id: str
    session_id: str
