import aioredis

class RedisTools:
    def __init__(self):
        self.rd = aioredis.from_url('redis://redis')

    async def set_pair(self, key: str, value: str):
        """
        Record creation method
        """
        await self.rd.set(key, value)

    async def get_pair(self, key: str):
        """
        Method for getting data by key
        """
        return await self.rd.get(key)

    async def delete_pair(self, key: str):
        """
        Method for delete data by key
        """
        return await self.rd.delete(key)

redis_tools = RedisTools()

