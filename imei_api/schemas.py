from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str


class UserDB(BaseModel):
    username: str
    token: str
