from fastapi import APIRouter
from schemas import AnalyticsResponse, StudentPublic
from services.students import (
    get_total_students,
    get_students_by_department,
    get_recent_onboarded_students,
    get_active_students_last_7_days,
)


router = APIRouter()


@router.get("/", response_model=AnalyticsResponse)
async def analytics_summary():
    total = await get_total_students()
    by_dept = await get_students_by_department()
    recent = await get_recent_onboarded_students(limit=5)
    active = await get_active_students_last_7_days()
    return {
        "total_students": total,
        "students_by_department": by_dept,
        "recent_onboarded": recent,
        "active_last_7_days": active,
    }


