import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from app.db.base_class import Base


class Post(Base):
    """
    Table for posts
    """
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(50))
    content = Column(String(2200))

    author_id = Column(Integer, ForeignKey("user.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
