from app.db.base_repository import BaseRepository
from app.models import Post
from sqlalchemy import delete

from app.redis_tools import redis_tools


class PostRepository(BaseRepository[Post]):
    async def remove(self, id: int):
        """
        Method for deleting a post and reactions to it
        """
        async with self.get_session() as session:
            await session.execute(delete(self.model).where(self.model.id == id))
            await session.commit()
            await redis_tools.delete_pair(str(id))

post = PostRepository(Post)
