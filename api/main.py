from fastapi import FastAPI, Depends, HTTPException, Response, status
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


@app.get("/heroes", status_code=status.HTTP_200_OK)
def get_heroes(db: Session = Depends(get_db)) -> dict:
    heroes = db.query(models.Hero).all()

    if not heroes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Heroes was not found."
        )

    return heroes


@app.get("/heroes/{name}", status_code=status.HTTP_200_OK, response_model=schemas.GetHero)
def get_hero_by_name(name: str, db: Session = Depends(get_db)) -> dict:
    hero = db.query(models.Hero).filter(models.Hero.name == name).first()

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with name {name} was not found.",
        )

    return hero


@app.post("/heroes/addhero", status_code=status.HTTP_201_CREATED)
def add_hero(request: schemas.Hero, db: Session = Depends(get_db)) -> dict:
    new_hero = models.Hero(
        name=request.name,
        wry_name=request.wry_name,
        role=request.role,
        description=request.description,
    )

    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)

    return {"data": f"Successfully create a hero {new_hero}"}


@app.put("/heroes/{name}", status_code=status.HTTP_202_ACCEPTED)
def update_hero(
    name: str, request: schemas.Hero, db: Session = Depends(get_db)
) -> dict:
    hero_to_update = db.query(models.Hero).filter(models.Hero.name == name)

    if hero_to_update.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with name {name} was not found",
        )

    hero_to_update.update(
        {
            "name": name,
            "wry_name": request.wry_name,
            "role": request.role,
            "description": request.description,
        },
        synchronize_session=False,
    )
    db.commit()

    return {"data": f"Hero with name {name} was updated"}


@app.delete("/heroes/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(name: str, db: Session = Depends(get_db)) -> dict:
    hero = db.query(models.Hero).filter(models.Hero.name == name)

    if hero.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with name {name} was not found",
        )

    hero.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)) -> dict:
    new_user = models.User(**request.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except BaseException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'user with email {request.email} is already exists.')
    
    return new_user
