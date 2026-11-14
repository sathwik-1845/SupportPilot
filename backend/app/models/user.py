# from sqlalchemy import Column, Integer, String
# from app.db.base import Base # Assuming you have a Base declarative_base here

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class RevokedToken(Base):
    """Logout denylist. Rows are safe to delete once expires_at has passed."""

    __tablename__ = "revoked_tokens"

    jti = Column(String(32), primary_key=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)