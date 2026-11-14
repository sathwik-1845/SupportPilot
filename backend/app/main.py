from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_v1_router
from app.core.config import get_settings
from app.models import tenant as _tenant_models  # noqa: F401  (register models on Base)
from app.models import user as _user_models  # noqa: F401

settings = get_settings()

# Tables are now managed by Alembic migrations (`alembic upgrade head`), not create_all.
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the SupportPilot API"}


app.include_router(api_v1_router.router, prefix="/api/v1")