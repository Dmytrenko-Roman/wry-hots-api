from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from repository import users
import schemas


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse
)
def get_user(id: int, db: Session = Depends(get_db)) -> dict:
    return users.get_by_id(id, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserBase, db: Session = Depends(get_db)) -> dict:
    return users.create(request, db)
