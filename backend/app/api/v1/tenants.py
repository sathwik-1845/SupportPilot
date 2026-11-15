from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_business_admin, require_tenant_member
from app.db.session import get_db
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.tenant import TenantOut, TenantUpdate

router = APIRouter()

_REQUIRED = ("business_name", "business_email", "industry")


def _own_tenant(db: Session, user: User) -> Tenant:
    tenant = db.get(Tenant, user.tenant_id)
    if tenant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return tenant


@router.get("/me", response_model=TenantOut)
def my_tenant(user: User = Depends(require_tenant_member), db: Session = Depends(get_db)):
    """The caller's own tenant. There is no /tenants/{id} for tenant users, so nothing to tamper with."""
    return _own_tenant(db, user)


@router.patch("/me", response_model=TenantOut)
def update_my_tenant(
    data: TenantUpdate, user: User = Depends(require_business_admin), db: Session = Depends(get_db)
):
    tenant = _own_tenant(db, user)  # tenant comes from the caller, never from the request
    updates = data.model_dump(exclude_unset=True)

    for field in _REQUIRED:
        if field in updates and updates[field] is None:
            raise HTTPException(422, f"{field} cannot be empty")

    new_email = updates.get("business_email")
    if new_email and new_email != tenant.business_email:
        if db.scalar(select(Tenant.id).where(Tenant.business_email == new_email, Tenant.id != tenant.id)):
            raise HTTPException(status.HTTP_409_CONFLICT, "Business email already registered")

    for field, value in updates.items():
        setattr(tenant, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Business email already registered") from None
    db.refresh(tenant)
    return tenant