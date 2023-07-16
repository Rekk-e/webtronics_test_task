import datetime

from sqlalchemy import Column, Integer, DateTime, String

from app.db.base_class import Base


class User(Base):
    """
    Table for users
    """
    id = Column(Integer, primary_key=True, index=True)

    fullname = Column(String, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
