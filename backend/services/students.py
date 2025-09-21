from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from bson import ObjectId
from db import get_students_collection, get_activity_collection
from schemas import StudentCreate, StudentUpdate, StudentPublic


def _serialize_student(doc: Dict[str, Any]) -> StudentPublic:
    return StudentPublic(
        id=str(doc.get("_id")),
        student_id=doc.get("student_id"),
        name=doc.get("name"),
        department=doc.get("department"),
        email=doc.get("email"),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
    )


async def add_student(data: StudentCreate) -> StudentPublic:
    coll = get_students_collection()
    now = datetime.utcnow()
    doc = data.model_dump()
    doc.update({"created_at": now, "updated_at": now})
    result = await coll.insert_one(doc)
    saved = await coll.find_one({"_id": result.inserted_id})
    
    # Log activity
    await get_activity_collection().insert_one({
        "student_id": data.student_id,
        "activity": "created",
        "timestamp": now,
    })
    
    # Send admin notification
    student_obj = _serialize_student(saved)
    try:
        from agent.tools import send_admin_notification
        send_admin_notification("created", student_obj.model_dump())
    except Exception as e:
        print(f"⚠️ Failed to send notification: {e}")
    
    return student_obj


async def get_student(student_id: str) -> Optional[StudentPublic]:
    coll = get_students_collection()
    doc = await coll.find_one({"student_id": student_id})
    return _serialize_student(doc) if doc else None


async def update_student(student_id: str, update: StudentUpdate) -> Optional[StudentPublic]:
    coll = get_students_collection()
    upd_doc = {k: v for k, v in update.model_dump(exclude_none=True).items()}
    if not upd_doc:
        doc = await coll.find_one({"student_id": student_id})
        return _serialize_student(doc) if doc else None
    upd_doc["updated_at"] = datetime.utcnow()
    doc = await coll.find_one_and_update(
        {"student_id": student_id},
        {"$set": upd_doc},
        return_document=True,
    )
    if doc:
        await get_activity_collection().insert_one({
            "student_id": student_id,
            "activity": "updated",
            "timestamp": datetime.utcnow(),
        })
        
        # Send admin notification
        student_obj = _serialize_student(doc)
        try:
            from agent.tools import send_admin_notification
            send_admin_notification("updated", student_obj.model_dump())
        except Exception as e:
            print(f"⚠️ Failed to send notification: {e}")
    
    return _serialize_student(doc) if doc else None


async def delete_student(student_id: str) -> bool:
    coll = get_students_collection()
    res = await coll.delete_one({"student_id": student_id})
    if res.deleted_count:
        now = datetime.utcnow()
        await get_activity_collection().insert_one({
            "student_id": student_id,
            "activity": "deleted",
            "timestamp": now,
        })
        
        # Send admin notification
        try:
            from agent.tools import send_admin_notification
            send_admin_notification("deleted", {
                "student_id": student_id,
                "deleted_at": now
            })
        except Exception as e:
            print(f"⚠️ Failed to send notification: {e}")
    
    return res.deleted_count > 0


async def list_students() -> List[StudentPublic]:
    coll = get_students_collection()
    cursor = coll.find().sort("created_at", -1)
    return [_serialize_student(doc) async for doc in cursor]


async def get_total_students() -> int:
    return await get_students_collection().count_documents({})


async def get_students_by_department() -> List[dict]:
    pipeline = [
        {"$group": {"_id": "$department", "count": {"$sum": 1}}},
        {"$project": {"department": "$_id", "count": 1, "_id": 0}},
        {"$sort": {"count": -1}},
    ]
    cursor = get_students_collection().aggregate(pipeline)
    return [doc async for doc in cursor]


async def get_recent_onboarded_students(limit: int = 5) -> List[StudentPublic]:
    coll = get_students_collection()
    cursor = coll.find().sort("created_at", -1).limit(limit)
    return [_serialize_student(doc) async for doc in cursor]


async def get_active_students_last_7_days() -> int:
    since = datetime.utcnow() - timedelta(days=7)
    coll = get_activity_collection()
    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {"_id": "$student_id"}},
        {"$count": "num"},
    ]
    cursor = coll.aggregate(pipeline)
    docs = [doc async for doc in cursor]
    return int(docs[0]["num"]) if docs else 0


