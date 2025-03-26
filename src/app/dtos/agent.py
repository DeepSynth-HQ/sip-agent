from pydantic import BaseModel
from typing import Optional


class AgentChatRequest(BaseModel):
    message: str
    images: list[str] = []
    stream: Optional[bool] = True
    session_id: str
