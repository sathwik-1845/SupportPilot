from sqlalchemy import Column, Integer, String
from app.db.base import Base # Assuming you have a Base declarative_base here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)