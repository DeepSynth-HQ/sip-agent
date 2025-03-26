from pydantic import BaseModel


class UserDefaultDto(BaseModel):
    id: str
    email: str
    name: str
    picture: str
    wallet_address: str
