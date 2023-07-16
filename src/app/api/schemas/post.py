from typing import Union, List

from pydantic import BaseModel
from pydantic.types import date

from app.api.schemas import Reaction


class PostTitle(str):
    """
    Data type for validate post title
    """
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError(f'str expected, got {type(v)}')
        if len(v) > 50:
            raise ValueError('The length of the title must be no more than 50 characters')

        return v

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class PostContent(str):
    """
    Data type for validate post content
    """
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError(f'str expected, got {type(v)}')
        if len(v) > 2200:
            raise ValueError('The length of the title must be no more than 2200 characters')

        return v

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class CreatePost(BaseModel):
    """
    Post creation schema.
    """
    title: PostTitle
    content: PostContent


class UpdatePost(BaseModel):
    """
    Post update schema.
    """
    title: Union[PostTitle, None]
    content: Union[PostContent, None]


class PostResponse(BaseModel):
    """
    Post response schema.
    """
    id: int
    title: str
    content: str
    author_id: int
    created_at: date
    reactions: List[Reaction] = []

