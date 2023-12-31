from app.db.base_class import Base
from app.db.session import engine


async def init_db() -> None:
    """
    Function is used to initialize the database
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
