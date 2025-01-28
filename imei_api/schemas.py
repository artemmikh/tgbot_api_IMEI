from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    tg_username: Optional[str]


class UserDB(BaseModel):
    username: str
    token: str
    tg_username: Optional[str]
