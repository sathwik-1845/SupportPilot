import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import RevokedToken, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def _credentials_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_token_payload(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> dict:
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    except jwt.PyJWTError:
        raise _credentials_error() from None

    if db.get(RevokedToken, payload["jti"]):
        raise _credentials_error()
    return payload


def get_current_user(
    payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)
) -> User:
    try:
        user_id = int(payload["sub"])
    except (ValueError, TypeError):
        raise _credentials_error() from None

    user = db.get(User, user_id)
    if user is None:
        raise _credentials_error()
    return user