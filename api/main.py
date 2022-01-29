from fastapi import FastAPI

app = FastAPI()


@app.get('/heroes')
def get_heroes() -> dict:
    return {'data': {'name': 'Arthas'}}


@app.get('/heroes/{name}')
def get_hero_by_name(name: str) -> dict:
    return {'data': name}


@app.post('/heroes/addhero')
def add_hero() -> dict:
    return {'data': 'Successfully create a hero'}


@app.put('/heroes/{name}')
def update_hero(name: str) -> dict:
    return {'data': f'hero with name {name} was updated'}


@app.delete('/heroes/{name}')
def delete_hero(name: str) -> dict:
    return {'data': f'hero with name {name} was deleted'}
