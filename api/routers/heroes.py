from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
import schemas, models

router = APIRouter(
    prefix='/heroes',
    tags=['heroes']
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_heroes(db: Session = Depends(get_db)) -> dict:
    heroes = db.query(models.Hero).all()

    if not heroes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Heroes was not found."
        )

    return heroes


@router.get("/{name}", status_code=status.HTTP_200_OK, response_model=schemas.HeroResponse)
def get_hero_by_name(name: str, db: Session = Depends(get_db)) -> dict:
    hero = db.query(models.Hero).filter(models.Hero.name == name).first()

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with name {name} was not found.",
        )

    return hero


@router.post("/addhero", status_code=status.HTTP_201_CREATED, response_model=schemas.HeroResponse)
def add_hero(request: schemas.HeroBase, db: Session = Depends(get_db)) -> dict:
    new_hero = models.Hero(
        name=request.name,
        wry_name=request.wry_name,
        role=request.role,
        description=request.description,
    )

    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)

    return new_hero


@router.put("/{name}", status_code=status.HTTP_202_ACCEPTED)
def update_hero(
    name: str, request: schemas.HeroBase, db: Session = Depends(get_db)
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


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
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