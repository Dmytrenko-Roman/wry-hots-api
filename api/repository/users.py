from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from hashing import Hash
import models, schemas


def get_by_id(id: int, db: Session) -> dict:
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id ({id}) was not found",
        )

    return user


def create(request: schemas.UserBase, db: Session) -> dict:
    new_user = models.User(**request.dict())

    hashed_pwd = Hash.hash(new_user.password)
    new_user.password = hashed_pwd

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except BaseException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user with email {request.email} is already exists.",
        )

    return new_user
