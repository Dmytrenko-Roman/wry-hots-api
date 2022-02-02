from typing import Optional, List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    password: str


class HeroBase(BaseModel):
    name: Optional[str]
    wry_name: str
    role: str
    description: str


class Hero(HeroBase):
    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    name: str
    email: str
    heroes: List[Hero] = []

    class Config:
        orm_mode = True


class HeroResponse(BaseModel):
    wry_name: str
    role: str
    description: str
    creator: UserResponse

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
