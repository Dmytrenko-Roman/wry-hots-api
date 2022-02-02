from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import token_settings
from schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": token_settings.access_token_expire_minutes})
    encoded_jwt = jwt.encode(to_encode, token_settings.secret_key, algorithm=token_settings.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, token_settings.secret_key, algorithms=[token_settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)
