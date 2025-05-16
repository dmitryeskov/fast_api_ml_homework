from pydantic import BaseModel


class Features(BaseModel):
    features: list[float]


class User(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
