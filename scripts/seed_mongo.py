import asyncio
import random
import sys
import os
from argparse import ArgumentParser
from datetime import datetime, timedelta
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

# Add parent directory to path so we can import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import get_settings


DEPARTMENTS = [
    "Computer Science",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Business Administration",
    "Psychology",
    "Mathematics",
    "Physics",
]


FIRST_NAMES = ["Aisha", "Ali", "Fatima", "Hassan", "Sara", "Bilal", "Noor", "Ahmed", "Zainab", "Usman"]
LAST_NAMES = ["Khan", "Ahmed", "Malik", "Hussain", "Raza", "Iqbal", "Siddiqui", "Sheikh", "Farooq", "Chaudhry"]


def random_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_email(name: str, i: int) -> str:
    user = name.lower().replace(" ", ".")
    domains = ["example.edu", "campus.edu", "uni.edu"]
    return f"{user}{i}@{random.choice(domains)}"


async def seed(num_students: int = 50):
    settings = get_settings()
    print(f"Connecting to MongoDB: {settings.db_uri}")
    print(f"Database: {settings.mongodb_db}")
    
    try:
        client = AsyncIOMotorClient(settings.db_uri)
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        db = client[settings.mongodb_db]
        students = db["students"]
        activity = db["activity_logs"]

        print("🗑️  Clearing existing data...")
        await students.delete_many({})
        await activity.delete_many({})
        print("✅ Existing data cleared!")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return

    now = datetime.utcnow()
    docs = []
    for i in range(num_students):
        name = random_name()
        sid = f"S{1000+i}"
        dept = random.choice(DEPARTMENTS)
        email = random_email(name, i)
        created_at = now - timedelta(days=random.randint(0, 60))
        docs.append({
            "student_id": sid,
            "name": name,
            "department": dept,
            "email": email,
            "created_at": created_at,
            "updated_at": created_at,
        })

    if docs:
        print(f"📝 Inserting {len(docs)} students...")
        await students.insert_many(docs)
        print("✅ Students inserted!")

    # random activity over last 30 days
    print("📊 Generating activity logs...")
    activities = []
    for d in docs:
        count = random.randint(0, 5)
        for _ in range(count):
            ts = now - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
            activities.append({
                "student_id": d["student_id"],
                "activity": random.choice(["login", "view", "update_profile", "enroll"]),
                "timestamp": ts,
            })

    if activities:
        print(f"📝 Inserting {len(activities)} activity logs...")
        await activity.insert_many(activities)
        print("✅ Activity logs inserted!")

    print(f"🎉 Successfully seeded {len(docs)} students and {len(activities)} activity logs!")
    client.close()


if __name__ == "__main__":
    parser = ArgumentParser(description="Seed MongoDB with random students and activity logs")
    parser.add_argument("--count", "-c", type=int, default=50, help="Number of students to create")
    args = parser.parse_args()
    asyncio.run(seed(args.count))


