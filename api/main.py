from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal
import schemas, models


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/heroes')
def get_heroes(db: Session = Depends(get_db)) -> dict:
    heroes = db.query(models.Hero).all()

    return {'data': heroes}


@app.get('/heroes/{name}')
def get_hero_by_name(name: str, db: Session = Depends(get_db)) -> dict:
    hero = db.query(models.Hero).filter(models.Hero.name == name).first()

    return {'data': hero}


@app.post('/heroes/addhero')
def add_hero(request: schemas.Hero, db: Session = Depends(get_db)) -> dict:
    new_hero = models.Hero(name=request.name, wry_name=request.wry_name, role=request.role, description=request.description)

    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)

    return {'data': f'Successfully create a hero {new_hero}'}


@app.put('/heroes/{name}')
def update_hero(name: str) -> dict:
    return {'data': f'hero with name {name} was updated'}


@app.delete('/heroes/{name}')
def delete_hero(name: str) -> dict:
    return {'data': f'hero with name {name} was deleted'}
