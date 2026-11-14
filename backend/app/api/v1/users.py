import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_business_admin
from app.core.security import get_password_hash
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter()


def _get_in_tenant_or_404(db: Session, admin: User, user_id: uuid.UUID) -> User:
    """THE isolation rule for user lookups: the tenant filter is part of the query itself.
    Another tenant's user is indistinguishable from a nonexistent one (404, not 403)."""
    user = db.scalar(select(User).where(User.id == user_id, User.tenant_id == admin.tenant_id))
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user


@router.get("", response_model=list[UserOut])
def list_users(admin: User = Depends(require_business_admin), db: Session = Depends(get_db)):
    stmt = select(User).where(User.tenant_id == admin.tenant_id).order_by(User.created_at)
    return db.scalars(stmt).all()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate, admin: User = Depends(require_business_admin), db: Session = Depends(get_db)
):
    if db.scalar(select(User.id).where(User.email == data.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    user = User(
        tenant_id=admin.tenant_id,  # always the caller's tenant, never from the request body
        full_name=data.full_name,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role=data.role,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered") from None
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: uuid.UUID, admin: User = Depends(require_business_admin), db: Session = Depends(get_db)
):
    return _get_in_tenant_or_404(db, admin, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: uuid.UUID, admin: User = Depends(require_business_admin), db: Session = Depends(get_db)
):
    if user_id == admin.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "You cannot delete your own account")
    user = _get_in_tenant_or_404(db, admin, user_id)
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)