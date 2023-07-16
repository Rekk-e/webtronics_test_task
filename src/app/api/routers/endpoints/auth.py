import re
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import repo, models
from app.api import schemas
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash

from app.api.schemas.user import AdditionalUserDataForm
from app.api.schemas.message import MessageResponse

from app.core.constants import EMAIL_REGEX

router = APIRouter()


@router.post("/registration", response_model=schemas.MessageResponse)
async def registration(
        form_data: OAuth2PasswordRequestForm = Depends(),
        additional_data: AdditionalUserDataForm = Depends()
) -> Any:
    """
    Endpoint for user registration.
    """
    if not re.match(EMAIL_REGEX, form_data.username):
        raise HTTPException(status_code=401, detail="Incorrect email")

    user = await repo.user.authenticate(
        email=form_data.username, password=form_data.password
    )
    if user:
        raise HTTPException(status_code=409, detail="User already exists")

    await repo.user.create(
        fullname=additional_data.fullname,
        email=form_data.username,
        hashed_password=get_password_hash(form_data.password),
    )

    return MessageResponse(message=f"User {form_data.username} was successfully registered")


@router.post("/access-token", response_model=schemas.TokenResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Endpoint for user authenticate
    """
    user = await repo.user.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.API_ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_token(
            user.id, expires_delta=access_token_expires, token_type="access"
        ),
    }


