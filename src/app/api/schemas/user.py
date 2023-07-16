from fastapi import Form
from pydantic import BaseModel
from pydantic.dataclasses import dataclass



@dataclass
class AdditionalUserDataForm:
    """
    Schema for adding additional information.
    """
    fullname: str = Form()


class CurrentUser(BaseModel):
    """
    Schema to represent the current user.
    """
    id: int
    email: str
    password: str
    fullname: str


class User(BaseModel):
    """
    Schema for return user.
    """
    id: int
    email: str
    password: str


