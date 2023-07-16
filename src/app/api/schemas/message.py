from pydantic.main import BaseModel


class MessageResponse(BaseModel):
    """
    Schema for returning a message.
    """
    message: str
