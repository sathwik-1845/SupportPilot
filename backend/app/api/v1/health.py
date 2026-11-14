from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/db")
def health_db(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"status": "ok", "database": "connected"}

# import logging

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import text
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import Session

# from app.db.session import get_db

# router = APIRouter(prefix="/health", tags=["health"])

# logger = logging.getLogger(__name__)


# @router.get("")
# def health():
#     return {"status": "ok"}


# @router.get("/db")
# def health_db(db: Session = Depends(get_db)):
#     try:
#         db.execute(text("SELECT 1"))
#         return {
#             "status": "ok",
#             "database": "connected"
#         }

#     except SQLAlchemyError:
#         logger.exception("Database health check failed")

#         raise HTTPException(
#             status_code=503,
#             detail="Database unavailable"
#         )
