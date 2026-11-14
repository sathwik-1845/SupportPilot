from fastapi import APIRouter

from app.api.v1 import admin, auth, health, tenants, users

router = APIRouter()

# health.router already has prefix="/health"
router.include_router(health.router)
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/users", tags=["Users (tenant-scoped)"])
router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
router.include_router(admin.router, prefix="/admin", tags=["Super Admin"])