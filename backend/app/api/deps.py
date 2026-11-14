import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.tenant import Tenant, TenantStatus
from app.models.user import RevokedToken, Role, User

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
            status.HTTP_401_UNAUTHORIZED,
            "Token has expired. Please log in again.",
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
    """Identity, role and tenant ALL come from the database row, never from token claims
    or the request body. A tampered or stale token can't change who you are or which tenant you're in."""
    try:
        user_id = uuid.UUID(payload["sub"])
    except (ValueError, TypeError):
        raise _credentials_error() from None

    user = db.get(User, user_id)
    if user is None:
        raise _credentials_error()

    # A suspended/cancelled tenant locks out all its users immediately, even with valid tokens.
    if user.tenant_id is not None:
        tenant = db.get(Tenant, user.tenant_id)
        if tenant is None or tenant.status != TenantStatus.ACTIVE:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Tenant account is not active")
    return user


def require_roles(*allowed: Role):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
        return user

    return checker


require_super_admin = require_roles(Role.SUPER_ADMIN)
require_business_admin = require_roles(Role.BUSINESS_ADMIN)
require_tenant_member = require_roles(Role.BUSINESS_ADMIN, Role.SUPPORT_AGENT)