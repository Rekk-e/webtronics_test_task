from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

from app.core.constants import ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(
        subject: Union[str, Any], token_type: str, expires_delta: timedelta = None
) -> str:
    """
    Creates a JWT token,
    including the specified data and expiration time,
    using the given secret key and encryption algorithm.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    To check for a match
    simple password and hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    For hashing password
    """
    return pwd_context.hash(password)
