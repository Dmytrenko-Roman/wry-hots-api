from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from repository import heroes
from oauth2 import get_current_user
import schemas

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_heroes(
    db: Session = Depends(get_db),
    get_current_user: schemas.UserBase = Depends(get_current_user),
) -> dict:
    return heroes.get_all(db)


@router.get(
    "/{name}", status_code=status.HTTP_200_OK, response_model=schemas.HeroResponse
)
def get_hero_by_name(name: str, db: Session = Depends(get_db)) -> dict:
    return heroes.get_by_name(name, db)


@router.post(
    "/addhero", status_code=status.HTTP_201_CREATED, response_model=schemas.HeroResponse
)
def add_hero(request: schemas.HeroBase, db: Session = Depends(get_db)) -> dict:
    return heroes.add(request, db)


@router.put("/{name}", status_code=status.HTTP_202_ACCEPTED)
def update_hero(
    name: str, request: schemas.HeroBase, db: Session = Depends(get_db)
) -> dict:
    return heroes.update(name, request, db)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(name: str, db: Session = Depends(get_db)) -> dict:
    return heroes.delete(name, db)
