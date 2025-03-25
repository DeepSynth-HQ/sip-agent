from typing import List, Optional
from agno.tools.x import XTools
from pydantic import BaseModel


class PostResponse(BaseModel):
    status: bool
    data: Optional[str]
    code: int


class XFunctions:
    @staticmethod
    def create_post(text: str, medias: List[str]) -> PostResponse:
        pass
