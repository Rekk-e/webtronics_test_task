from typing import Optional

from app.db.base_repository import BaseRepository
from app.models import Reaction
from app.redis_tools.tools import redis_tools
from app.db.base_repository import ModelType
from sqlalchemy import select
from app.api.utils.reactions import serialize
from app.api.utils.reactions import deserialize


class ReactionRepository(BaseRepository[Reaction]):
    async def get_by_post(self, post_id: int) -> Optional[ModelType]:
        """
        Method for getting reactions to a post
        """

        # Return data from redis if exists
        reactions = await redis_tools.get_pair(str(post_id))
        if reactions:
            return deserialize(reactions, Reaction)

        async with self.get_session() as session:
            result = await session.execute(select(self.model).where(self.model.post_id == post_id))
            return result.scalars().all()

    async def update_reactions(self, post_id: int):
        """
        Method for caching post reactions
        """
        async with self.get_session() as session:
            result = await session.execute(select(self.model).where(self.model.post_id == post_id))
            serialize_result = serialize(result.scalars().all())
            if serialize_result:
                await redis_tools.set_pair(str(post_id), serialize_result)


reaction = ReactionRepository(Reaction)
