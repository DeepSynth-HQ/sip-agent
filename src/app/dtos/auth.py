from .user import UserDefaultDto
from pydantic import BaseModel, ConfigDict


class AuthResponseDto(BaseModel):
    access_token: str
    refresh_token: str


class LoginResponseDto(BaseModel):
    user: UserDefaultDto
    model_config = ConfigDict(arbitrary_types_allowed=True)
