from datetime import datetime, timezone
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from models.user import UserCreate, UserUpdate, UserInDB, serialize_user_in_db, serialize_user
from services.auth import get_password_hash


async def create_user(db: AsyncIOMotorDatabase, user_create: UserCreate) -> UserInDB:
    """Create a new user."""
    now = datetime.now(timezone.utc)
    
    user_doc = {
        "email": user_create.email,
        "username": user_create.username,
        "full_name": user_create.full_name,
        "hashed_password": get_password_hash(user_create.password),
        "is_active": user_create.is_active,
        "is_admin": user_create.is_admin,
        "created_at": now,
        "updated_at": now,
    }
    
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    return serialize_user_in_db(user_doc)


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserInDB]:
    """Get user by ID."""
    from bson import ObjectId
    
    try:
        user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            return serialize_user_in_db(user_doc)
    except Exception:
        pass
    return None


async def get_user_by_username(db: AsyncIOMotorDatabase, username: str) -> Optional[UserInDB]:
    """Get user by username."""
    user_doc = await db.users.find_one({"username": username})
    if user_doc:
        return serialize_user_in_db(user_doc)
    return None


async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> Optional[UserInDB]:
    """Get user by email."""
    user_doc = await db.users.find_one({"email": email})
    if user_doc:
        return serialize_user_in_db(user_doc)
    return None


async def update_user(db: AsyncIOMotorDatabase, user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
    """Update user."""
    from bson import ObjectId
    
    update_data = {}
    if user_update.email is not None:
        update_data["email"] = user_update.email
    if user_update.username is not None:
        update_data["username"] = user_update.username
    if user_update.full_name is not None:
        update_data["full_name"] = user_update.full_name
    if user_update.password is not None:
        update_data["hashed_password"] = get_password_hash(user_update.password)
    if user_update.is_active is not None:
        update_data["is_active"] = user_update.is_active
    if user_update.is_admin is not None:
        update_data["is_admin"] = user_update.is_admin
    
    if not update_data:
        return None
    
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    try:
        user_doc = await db.users.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        if user_doc:
            return serialize_user_in_db(user_doc)
    except Exception:
        pass
    return None


async def delete_user(db: AsyncIOMotorDatabase, user_id: str) -> bool:
    """Delete user."""
    from bson import ObjectId
    
    try:
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception:
        return False
