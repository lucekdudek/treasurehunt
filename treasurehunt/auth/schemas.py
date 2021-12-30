from pydantic import BaseModel


class APIAuthIn(BaseModel):
    username: str
    password: str


class APIPostLoginOut(BaseModel):
    token: str


class AuthDetails(BaseModel):
    user_id: str
    hash: str
