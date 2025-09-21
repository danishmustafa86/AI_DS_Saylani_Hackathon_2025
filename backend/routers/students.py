from fastapi import APIRouter, HTTPException
from schemas import StudentCreate, StudentUpdate, StudentPublic
from services.students import (
    add_student as svc_add_student,
    get_student as svc_get_student,
    update_student as svc_update_student,
    delete_student as svc_delete_student,
    list_students as svc_list_students,
)


router = APIRouter()


@router.post("/", response_model=StudentPublic)
async def add_student(payload: StudentCreate):
    existing = await svc_get_student(payload.student_id)
    if existing:
        raise HTTPException(status_code=400, detail="Student already exists")
    return await svc_add_student(payload)


@router.get("/{student_id}", response_model=StudentPublic)
async def get_student(student_id: str):
    student = await svc_get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentPublic)
async def update_student(student_id: str, payload: StudentUpdate):
    student = await svc_update_student(student_id, payload)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
async def delete_student(student_id: str):
    ok = await svc_delete_student(student_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"deleted": True}


@router.get("/", response_model=list[StudentPublic])
async def list_students():
    return await svc_list_students()


