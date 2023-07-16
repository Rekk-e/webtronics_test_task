import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM



class Reaction(Base):
    """
    Table for reactions
    """
    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(Integer, ForeignKey("post.id"))
    author_id = Column(Integer, ForeignKey("user.id"))

    reaction = Column(ENUM("Like", "Dislike", name='Reactions'))

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
