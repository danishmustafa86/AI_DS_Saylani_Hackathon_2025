from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from settings import get_settings


class MongoClientManager:
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            settings = get_settings()
            cls._client = AsyncIOMotorClient(settings.db_uri)
        return cls._client

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        if cls._db is None:
            settings = get_settings()
            cls._db = cls.get_client()[settings.mongodb_db]
        return cls._db


def get_students_collection():
    return MongoClientManager.get_db()["students"]


def get_activity_collection():
    return MongoClientManager.get_db()["activity_logs"]


def get_chat_history_collection():
    return MongoClientManager.get_db()["chat_history"]


def get_database() -> AsyncIOMotorDatabase:
    """Get the database instance - alias for get_db"""
    return MongoClientManager.get_db()


def get_users_collection():
    """Get users collection"""
    return MongoClientManager.get_db()["users"]

