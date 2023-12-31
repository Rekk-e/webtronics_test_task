from fastapi import APIRouter
from .endpoints import auth, post

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(post.router, prefix="/post", tags=["posts"])

