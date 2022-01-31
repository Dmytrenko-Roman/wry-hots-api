from typing import Optional

from pydantic import BaseModel


class Hero(BaseModel):
    name: Optional[str]
    wry_name: str
    role: str
    description: str


class GetHero(BaseModel):
    wry_name: str
    role: str
    description: str
    
    class Config:
        orm_mode = True
