from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from hashing import Hash
import schemas, models, hashing


router = APIRouter(
    tags=['authentication']
)


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)) -> dict:
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ivalid Credentials")

    if not hashing.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    return user
