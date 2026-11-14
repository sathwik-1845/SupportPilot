from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_token_payload
from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.session import get_db
from app.models.tenant import Tenant, TenantStatus
from app.models.user import RevokedToken, Role, User
from app.schemas.user import BusinessRegister, BusinessRegisterOut, Token, UserOut

router = APIRouter()


@router.post("/register-business", response_model=BusinessRegisterOut, status_code=status.HTTP_201_CREATED)
def register_business(data: BusinessRegister, db: Session = Depends(get_db)):
    """Creates the tenant and its first Business Admin atomically (all or nothing)."""
    if db.scalar(select(Tenant.id).where(Tenant.business_email == data.business_email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Business email already registered")
    if db.scalar(select(User.id).where(User.email == data.admin_email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    tenant = Tenant(
        business_name=data.business_name,
        business_email=data.business_email,
        industry=data.industry,
    )
    db.add(tenant)
    db.flush()  # assigns tenant.id

    admin = User(
        tenant_id=tenant.id,
        full_name=data.admin_full_name,
        email=data.admin_email,
        hashed_password=get_password_hash(data.password),
        role=Role.BUSINESS_ADMIN,
    )
    db.add(admin)
    try:
        db.commit()
    except IntegrityError:  # concurrent duplicate
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered") from None
    db.refresh(tenant)
    db.refresh(admin)
    return BusinessRegisterOut(tenant=tenant, user=admin)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username.strip().lower()  # form field "username" carries the email
    user = db.scalar(select(User).where(User.email == email))

    # Always verify a hash so timing doesn't reveal whether the email exists
    ok = verify_password(form_data.password, user.hashed_password if user else DUMMY_HASH)
    if not user or not ok:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.tenant_id is not None:
        tenant = db.get(Tenant, user.tenant_id)
        if tenant is None or tenant.status != TenantStatus.ACTIVE:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Tenant account is not active")

    token, expires_in = create_access_token(user.id)
    return Token(access_token=token, expires_in=expires_in)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    db.add(
        RevokedToken(
            jti=payload["jti"],
            expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
        )
    )
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user