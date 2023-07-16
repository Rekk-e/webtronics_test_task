from typing import Optional

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Token response schema.
    """
    access_token: str


class TokenPayload(BaseModel):
    """
    Token payload schema.
    """
    sub: Optional[int] = None
    type: Optional[str] = None
