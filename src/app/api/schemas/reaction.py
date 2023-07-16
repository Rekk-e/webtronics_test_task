from pydantic.main import BaseModel
from pydantic.types import date

from app.api.utils.enums import ReactionTypes


class Reaction(BaseModel):
    """
    Post reactions schema.
    """
    author_id: int
    reaction: ReactionTypes
    created_at: date
