from jose import jwt, JWTError
from fastapi import HTTPException

from config import token_settings
from schemas import TokenData


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": token_settings.access_token_expire_minutes})
    encoded_jwt = jwt.encode(
        to_encode, token_settings.secret_key, algorithm=token_settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception: HTTPException) -> None:
    try:
        payload = jwt.decode(
            token, token_settings.secret_key, algorithms=[token_settings.algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
