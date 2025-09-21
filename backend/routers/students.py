from fastapi import APIRouter, HTTPException
from schemas import StudentCreate, StudentUpdate, StudentPublic, AnalyticsResponse
from services.students import (
    add_student as svc_add_student,
    get_student as svc_get_student,
    update_student as svc_update_student,
    delete_student as svc_delete_student,
    list_students as svc_list_students,
    get_total_students,
    get_students_by_department,
    get_recent_onboarded_students,
    get_active_students_last_7_days,
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


@router.get("/analytics/overview", response_model=AnalyticsResponse)
async def get_students_analytics():
    """Get comprehensive student analytics data"""
    return AnalyticsResponse(
        total_students=await get_total_students(),
        students_by_department=await get_students_by_department(),
        recent_onboarded=await get_recent_onboarded_students(),
        active_last_7_days=await get_active_students_last_7_days()
    )


