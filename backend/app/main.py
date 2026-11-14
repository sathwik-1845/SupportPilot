from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_v1_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.models import user as _user_models  # noqa: F401  (registers tables on Base)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev convenience: creates missing tables (users, revoked_tokens).
    # It never ALTERs existing tables. Switch to Alembic migrations before you change columns.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

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