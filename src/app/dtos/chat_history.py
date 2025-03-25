from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal
import uuid


class Message(BaseModel):
    role: Literal["user", "assistant", "reasoning"]
    content: str
    images: list[str] | None = None


class ChatHistoryDTO(BaseModel):
    title: str
    data: list[Message] | None = None
    created_at: datetime
    session_id: str


class UpdateTitleRequest(BaseModel):
    title: str = Field(
        description="The title to be updated",
        examples=["My first session"],
    )
    session_id: str = Field(
        description="The session id",
        examples=[str(uuid.uuid4())],
    )
