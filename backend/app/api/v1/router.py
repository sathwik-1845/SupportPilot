from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1 import auth
# This creates the exact variable named 'router'
router = APIRouter()

# A test endpoint to prove it works
@router.get("/health")
def health_check():
    return {"message": "SupportPilot API is running!"}

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@router.get("/health/db")
def db_health_check():
    # You will eventually put real database connection logic here
    return {"status": "pending", "message": "Database connection not yet configured"}