import os
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class Database(AsyncIOMotorDatabase):
    client = AsyncIOMotorClient(os.getenv("DATABASE_URI"))

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f"Use {cls.__name__}.connect() instead of direct instantiation.")

    @classmethod
    async def ping(cls):
        await cls.client.admin.command("ping")

    @classmethod
    def connect(cls):
        try:
            asyncio.run(cls.ping())
        except Exception as e:
            raise RuntimeError(f"Failed to connect to the database: {e}")

        name = os.getenv("DATABASE_NAME")
        if name is None:
            raise ValueError("Missing required environment variable: 'DATABASE_NAME'")

        # Bypass __new__ restriction to allow controlled instantiation
        # Using object.__new__(cls) directly avoids calling Database.__new__()
        self = object.__new__(cls)
        super().__init__(self, cls.client, name)
        return self
