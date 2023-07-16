from typing import Optional

from sqlalchemy import select

from app.core.security import verify_password
from app.db.base_repository import BaseRepository
from app.models import User


class UserRepository(BaseRepository[User]):
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Method to get user by email
        """
        async with self.get_session() as session:
            result = await session.execute(select(self.model).where(self.model.email == email))
            return result.scalars().first()

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Method for user authentication
        """
        db_obj = await self.get_by_email(email=email)
        if not db_obj or (db_obj and not verify_password(password, db_obj.hashed_password)):
            return None

        return db_obj


user = UserRepository(User)
