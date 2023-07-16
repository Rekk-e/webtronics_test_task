
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import repo, models
from app.api.deps.login import get_current_user
from app.api.schemas import CreatePost, UpdatePost, PostResponse
from app.api.utils.enums import ReactionTypes

from app.api.schemas.user import CurrentUser
from app.api.schemas.message import MessageResponse

from app.api.utils.reactions import get_reactions

router = APIRouter()

from urllib.parse import quote

@router.get("/encode_url")
def test_router(url: str):
    encoded_url = quote(url, safe="")
    return encoded_url


@router.post("", response_model=PostResponse, dependencies=[Depends(get_current_user)])
async def create_post(form_data: CreatePost, current_user: CurrentUser = Depends(get_current_user)) -> Any:
    """
    Endpoint for creating a post
    """
    post = await repo.post.create(
        title=form_data.title,
        content=form_data.content,
        author_id=current_user.id,
    )
    if not post:
        raise HTTPException(status_code=400, detail="Post create error")

    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        created_at=post.created_at
    )


@router.get("", response_model=List[PostResponse], dependencies=[Depends(get_current_user)])
async def get_posts() -> Any:
    """
    Endpoint for get all posts
    """
    posts = await repo.post.get_all()
    post_models = list()
    for post in posts:
        reactions = await get_reactions(post.id)
        post_model = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            author_id=post.author_id,
            created_at=post.created_at,
            reactions=reactions
        )
        post_models.append(post_model)

    return post_models


@router.get("/{post_id}", response_model=PostResponse, dependencies=[Depends(get_current_user)])
async def get_post(post_id: int) -> Any:
    """
    Endpoint for get a post
    """
    post = await repo.post.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    reactions = await get_reactions(post_id)

    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        created_at=post.created_at,
        reactions=reactions
    )


@router.patch("/{post_id}", response_model=MessageResponse, dependencies=[Depends(get_current_user)])
async def update_post(post_id: int, form_data: UpdatePost, current_user: CurrentUser = Depends(get_current_user)) -> Any:
    """
    Endpoint for updating post
    """
    post = await repo.post.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if current_user.id != post.author_id:
        raise HTTPException(status_code=403, detail="Only the author of a post can edit it")

    await repo.post.update(db_obj=post, title=form_data.title, content=form_data.content)

    return MessageResponse(message=f"Post with id {post_id} has been updated")


@router.delete("/{post_id}", response_model=MessageResponse, dependencies=[Depends(get_current_user)])
async def remove_post(post_id: int, current_user: CurrentUser = Depends(get_current_user)) -> Any:
    """
    Endpoint to delete post
    """
    post = await repo.post.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if current_user.id != post.author_id:
        raise HTTPException(status_code=403, detail="Only the author of a post can delete it")

    await repo.post.remove(post_id)

    return MessageResponse(message=f"Post with id {post_id} has been deleted")


@router.post("/{post_id}/reactions/{reaction}", response_model=MessageResponse, dependencies=[Depends(get_current_user)])
async def send_reaction(post_id: int, reaction: ReactionTypes, current_user: CurrentUser = Depends(get_current_user)) -> Any:
    """
    Endpoint to send post reaction
    """
    post = await repo.post.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if current_user.id == post.author_id:
        raise HTTPException(status_code=403, detail="Post author can't send reactions")

    # Getting all the reactions to a post and searching among them for the user's reaction
    reactions = await repo.reaction.get_by_post(post_id)
    if str(current_user.id) in [reaction.author_id for reaction in reactions]:
        raise HTTPException(status_code=422, detail="User cannot send more than one reaction per post")

    await repo.reaction.create(
        post_id=post_id,
        author_id=current_user.id,
        reaction=reaction.value
    )
    await repo.reaction.update_reactions(post_id=post_id)

    return MessageResponse(message=f"Reaction to post {post_id} has been sent")