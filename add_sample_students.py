#!/usr/bin/env python3
"""
Script to add sample students to the database for testing
"""
import asyncio
from services.students import add_student
from schemas import StudentCreate

sample_students = [
    StudentCreate(
        student_id="CS2021001",
        name="Alice Johnson",
        department="Computer Science",
        email="alice.johnson@university.edu"
    ),
    StudentCreate(
        student_id="EE2021002",
        name="Bob Smith",
        department="Electrical Engineering",
        email="bob.smith@university.edu"
    ),
    StudentCreate(
        student_id="ME2021003",
        name="Carol Davis",
        department="Mechanical Engineering",
        email="carol.davis@university.edu"
    ),
    StudentCreate(
        student_id="CS2021004",
        name="David Wilson",
        department="Computer Science",
        email="david.wilson@university.edu"
    ),
    StudentCreate(
        student_id="BIO2021005",
        name="Eva Brown",
        department="Biology",
        email="eva.brown@university.edu"
    ),
    StudentCreate(
        student_id="MATH2021006",
        name="Frank Miller",
        department="Mathematics",
        email="frank.miller@university.edu"
    ),
    StudentCreate(
        student_id="PHY2021007",
        name="Grace Taylor",
        department="Physics",
        email="grace.taylor@university.edu"
    ),
    StudentCreate(
        student_id="CS2021008",
        name="Henry Anderson",
        department="Computer Science",
        email="henry.anderson@university.edu"
    ),
    StudentCreate(
        student_id="EE2021009",
        name="Ivy Thomas",
        department="Electrical Engineering",
        email="ivy.thomas@university.edu"
    ),
    StudentCreate(
        student_id="CHEM2021010",
        name="Jack Wilson",
        department="Chemistry",
        email="jack.wilson@university.edu"
    ),
]

async def add_sample_data():
    """Add sample students to the database"""
    print("Adding sample students...")
    
    for student in sample_students:
        try:
            # Check if student already exists
            from services.students import get_student
            existing = await get_student(student.student_id)
            if existing:
                print(f"Student {student.student_id} already exists, skipping...")
                continue
                
            # Add the student
            result = await add_student(student)
            print(f"✅ Added student: {result.name} ({result.student_id})")
        except Exception as e:
            print(f"❌ Failed to add student {student.student_id}: {e}")
    
    print("Sample data creation complete!")

if __name__ == "__main__":
    asyncio.run(add_sample_data())
