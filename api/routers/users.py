from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
import schemas, models, hashing


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserBase, db: Session = Depends(get_db)) -> dict:
    new_user = models.User(**request.dict())

    hashed_pwd = hashing.hash(new_user.password)
    new_user.password = hashed_pwd

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except BaseException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'user with email {request.email} is already exists.')
    
    return new_user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)) -> dict:
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'user with id ({id}) was not found')

    return user
