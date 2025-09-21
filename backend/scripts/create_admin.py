#!/usr/bin/env python3
"""
Script to create an admin user in the database.
Usage: poetry run python scripts/create_admin.py
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_database
from models.user import UserCreate
from services.users import create_user, get_user_by_username


async def create_admin_user():
    """Create an admin user."""
    print("🔧 Creating Admin User")
    print("=" * 30)
    
    db = await get_database()
    
    # Check if admin already exists
    existing_admin = await get_user_by_username(db, "admin")
    if existing_admin:
        print("❌ Admin user already exists!")
        return
    
    # Create admin user
    admin_data = UserCreate(
        email="admin@campus.edu",
        username="admin",
        password="admin123",  # Change this in production!
        full_name="Campus Administrator",
        is_active=True,
        is_admin=True
    )
    
    try:
        admin_user = await create_user(db, admin_data)
        print(f"✅ Admin user created successfully!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   ID: {admin_user.id}")
        print("\n⚠️  Default password is 'admin123' - please change it!")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")


if __name__ == "__main__":
    asyncio.run(create_admin_user())
