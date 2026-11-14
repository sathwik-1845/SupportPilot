from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_tenant_member
from app.db.session import get_db
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.tenant import TenantOut

router = APIRouter()


@router.get("/me", response_model=TenantOut)
def my_tenant(user: User = Depends(require_tenant_member), db: Session = Depends(get_db)):
    """The caller's own tenant. There is no /tenants/{id} for tenant users, so nothing to tamper with."""
    tenant = db.get(Tenant, user.tenant_id)
    if tenant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tenant not found")
    return tenant