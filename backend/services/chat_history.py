from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from db import get_chat_history_collection
from schemas import ChatHistoryEntry, ChatHistoryResponse


def _serialize_chat_entry(doc: Dict[str, Any]) -> ChatHistoryEntry:
    """Convert MongoDB document to ChatHistoryEntry"""
    return ChatHistoryEntry(
        id=str(doc.get("_id")),
        user_id=doc.get("user_id"),
        session_id=doc.get("session_id"),
        user_message=doc.get("user_message"),
        ai_response=doc.get("ai_response"),
        timestamp=doc.get("timestamp"),
        created_at=doc.get("created_at"),
    )


async def save_chat_entry(
    user_id: str,
    session_id: str,
    user_message: str,
    ai_response: str
) -> ChatHistoryEntry:
    """Save a new chat entry to MongoDB"""
    collection = get_chat_history_collection()
    now = datetime.utcnow()
    
    doc = {
        "user_id": user_id,
        "session_id": session_id,
        "user_message": user_message,
        "ai_response": ai_response,
        "timestamp": now,
        "created_at": now,
    }
    
    result = await collection.insert_one(doc)
    saved_doc = await collection.find_one({"_id": result.inserted_id})
    
    # Keep only last 10 chats per user
    await _cleanup_old_chats(user_id)
    
    return _serialize_chat_entry(saved_doc)


async def _cleanup_old_chats(user_id: str, max_chats: int = 10):
    """Keep only the last N chats for a user"""
    collection = get_chat_history_collection()
    
    # Count total chats for user
    total_chats = await collection.count_documents({"user_id": user_id})
    
    if total_chats > max_chats:
        # Find oldest chats to delete
        chats_to_delete = total_chats - max_chats
        
        # Get oldest chat IDs
        cursor = collection.find(
            {"user_id": user_id}
        ).sort("created_at", 1).limit(chats_to_delete)
        
        old_chat_ids = [doc["_id"] async for doc in cursor]
        
        # Delete old chats
        if old_chat_ids:
            await collection.delete_many({"_id": {"$in": old_chat_ids}})
            print(f"🧹 Cleaned up {len(old_chat_ids)} old chats for user {user_id}")


async def get_user_chat_history(user_id: str, limit: int = 10) -> ChatHistoryResponse:
    """Get chat history for a user (last N chats)"""
    collection = get_chat_history_collection()
    
    # Get chats sorted by most recent first
    cursor = collection.find(
        {"user_id": user_id}
    ).sort("created_at", -1).limit(limit)
    
    chats = [_serialize_chat_entry(doc) async for doc in cursor]
    total_chats = await collection.count_documents({"user_id": user_id})
    
    return ChatHistoryResponse(
        user_id=user_id,
        total_chats=total_chats,
        chats=chats
    )


async def get_user_session_history(user_id: str, session_id: str) -> List[ChatHistoryEntry]:
    """Get all chats for a specific user session"""
    collection = get_chat_history_collection()
    
    cursor = collection.find({
        "user_id": user_id,
        "session_id": session_id
    }).sort("created_at", 1)  # Oldest first for conversation flow
    
    return [_serialize_chat_entry(doc) async for doc in cursor]


async def delete_user_chat_history(user_id: str) -> int:
    """Delete all chat history for a user"""
    collection = get_chat_history_collection()
    result = await collection.delete_many({"user_id": user_id})
    return result.deleted_count


async def get_recent_users_with_chats(limit: int = 20) -> List[Dict[str, Any]]:
    """Get list of users who have recent chat history"""
    collection = get_chat_history_collection()
    
    pipeline = [
        {
            "$group": {
                "_id": "$user_id",
                "last_chat": {"$max": "$created_at"},
                "total_chats": {"$sum": 1}
            }
        },
        {
            "$sort": {"last_chat": -1}
        },
        {
            "$limit": limit
        },
        {
            "$project": {
                "user_id": "$_id",
                "last_chat": 1,
                "total_chats": 1,
                "_id": 0
            }
        }
    ]
    
    cursor = collection.aggregate(pipeline)
    return [doc async for doc in cursor]


async def get_chat_statistics() -> Dict[str, Any]:
    """Get overall chat statistics"""
    collection = get_chat_history_collection()
    
    total_chats = await collection.count_documents({})
    total_users = len(await collection.distinct("user_id"))
    
    # Get chat count by date (last 7 days)
    from datetime import timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    recent_chats = await collection.count_documents({
        "created_at": {"$gte": week_ago}
    })
    
    return {
        "total_chats": total_chats,
        "total_users": total_users,
        "recent_chats_7_days": recent_chats,
        "avg_chats_per_user": round(total_chats / total_users, 2) if total_users > 0 else 0
    }
