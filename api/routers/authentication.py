from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from hashing import Hash
import models, auth_token


router = APIRouter(tags=["authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    user = db.query(models.User).filter(models.User.name == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )

    access_token = auth_token.create_access_token(data={"sub": user.name})

    return {"access_token": access_token, "token_type": "bearer"}
