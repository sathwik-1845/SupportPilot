import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_super_admin
from app.db.session import get_db
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.tenant import TenantOut, TenantStatusUpdate

# Every route here is Super Admin only: the dependency is applied to the whole router.
router = APIRouter(dependencies=[Depends(require_super_admin)])


@router.get("/tenants", response_model=list[TenantOut])
def list_tenants(db: Session = Depends(get_db)):
    return db.scalars(select(Tenant).order_by(Tenant.created_at)).all()


@router.get("/tenants/{tenant_id}", response_model=TenantOut)
def get_tenant(tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    tenant = db.get(Tenant, tenant_id)
    if tenant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return tenant


@router.patch("/tenants/{tenant_id}/status", response_model=TenantOut)
def set_tenant_status(
    tenant_id: uuid.UUID,
    data: TenantStatusUpdate,
    db: Session = Depends(get_db),
):
    tenant = db.get(Tenant, tenant_id)
    if tenant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    tenant.status = data.status
    db.commit()
    db.refresh(tenant)
    return tenant