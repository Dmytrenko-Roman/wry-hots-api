from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Hero(BaseModel):
    name: Optional[str]
    wry_name: str
    role: str
    description: str


@app.get('/heroes')
def get_heroes() -> dict:
    return {'data': {'name': 'Arthas'}}


@app.get('/heroes/{name}')
def get_hero_by_name(name: str) -> dict:
    return {'data': name}


@app.post('/heroes/addhero')
def add_hero(request: Hero) -> dict:
    return {'data': f'Successfully create a hero {request}'}


@app.put('/heroes/{name}')
def update_hero(name: str) -> dict:
    return {'data': f'hero with name {name} was updated'}


@app.delete('/heroes/{name}')
def delete_hero(name: str) -> dict:
    return {'data': f'hero with name {name} was deleted'}
