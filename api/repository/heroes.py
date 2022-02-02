from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

import models, schemas


def get_all(db: Session) -> dict:
    heroes = db.query(models.Hero).all()

    if not heroes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Heroes was not found."
        )

    return heroes


def get_by_name(name: str, db: Session) -> dict:
    hero = db.query(models.Hero).filter(models.Hero.name == name).first()

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with name {name} was not found.",
        )

    return hero


def add(request: schemas.HeroBase, db: Session, current_user: models.User) -> dict:
    new_hero = models.Hero(
        name=request.name,
        wry_name=request.wry_name,
        role=request.role,
        description=request.description,
        user_id=current_user.id
    )

    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)

    return new_hero


def update(name: str, request: schemas.HeroBase, db: Session) -> dict:
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


def delete(name: str, db: Session) -> dict:
    hero = db.query(models.Hero).filter(models.Hero.name == name)

    if hero.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with name {name} was not found",
        )

    hero.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_404_NOT_FOUND)
