from typing import Any, Dict, List
from langchain_core.tools import tool
from schemas import StudentCreate, StudentUpdate
from services import students as student_service


@tool("add_student")
async def tool_add_student(name: str, id: str, department: str, email: str) -> Dict[str, Any]:
    """Add a student with name, id, department, email."""
    payload = StudentCreate(student_id=id, name=name, department=department, email=email)
    student = await student_service.add_student(payload)
    return student.model_dump()


@tool("get_student")
async def tool_get_student(id: str) -> Dict[str, Any]:
    """Get a student by id."""
    student = await student_service.get_student(id)
    return student.model_dump() if student else {}


@tool("update_student")
async def tool_update_student(id: str, field: str, new_value: str) -> Dict[str, Any]:
    """Update a student's field to a new_value."""
    if field not in {"name", "department", "email"}:
        return {"error": "Invalid field"}
    update = StudentUpdate(**{field: new_value})
    student = await student_service.update_student(id, update)
    return student.model_dump() if student else {}


@tool("delete_student")
async def tool_delete_student(id: str) -> Dict[str, Any]:
    """Delete a student by id."""
    ok = await student_service.delete_student(id)
    return {"deleted": ok}


@tool("list_students")
async def tool_list_students() -> List[Dict[str, Any]]:
    """List all students."""
    students = await student_service.list_students()
    return [s.model_dump() for s in students]


@tool("get_total_students")
async def tool_get_total_students() -> int:
    """Get the total number of students."""
    return await student_service.get_total_students()


@tool("get_students_by_department")
async def tool_get_students_by_department() -> Dict[str, Any]:
    """Get count of students grouped by department in a user-friendly format."""
    try:
        data = await student_service.get_students_by_department()
        
        # Format for better readability
        formatted = {
            "summary": f"We have students across {len(data)} departments",
            "departments": data,
            "top_department": data[0]["department"] if data else "None",
            "top_count": data[0]["count"] if data else 0
        }
        return formatted
    except Exception as e:
        return {"error": f"Failed to get department data: {str(e)}"}


@tool("get_students_count_by_specific_department")
async def tool_get_students_count_by_specific_department(department_name: str) -> Dict[str, Any]:
    """Get count of students in a specific department by name (e.g., 'Computer Science')."""
    try:
        print(f"🔍 DEBUG: Searching for department: {department_name}")
        all_departments = await student_service.get_students_by_department()
        print(f"📊 DEBUG: Found {len(all_departments)} departments: {[d['department'] for d in all_departments]}")
        
        # Find the specific department (case-insensitive)
        department_name_lower = department_name.lower()
        for dept in all_departments:
            if dept["department"].lower() == department_name_lower:
                result = {
                    "department": dept["department"],
                    "count": dept["count"],
                    "message": f"There are {dept['count']} students enrolled in {dept['department']}"
                }
                print(f"✅ DEBUG: Found match: {result}")
                return result
        
        # If not found, return available departments
        available_depts = [d["department"] for d in all_departments]
        result = {
            "department": department_name,
            "count": 0,
            "message": f"No students found in '{department_name}'. Available departments: {', '.join(available_depts)}"
        }
        print(f"❌ DEBUG: No match found: {result}")
        return result
    except Exception as e:
        error_msg = f"Failed to get department data: {str(e)}"
        print(f"💥 DEBUG: Error occurred: {error_msg}")
        return {"error": error_msg}


@tool("get_recent_onboarded_students")
async def tool_get_recent_onboarded_students(limit: int = 5) -> List[Dict[str, Any]]:
    """Get recently onboarded students with optional limit."""
    students = await student_service.get_recent_onboarded_students(limit)
    return [s.model_dump() for s in students]


@tool("get_active_students_last_7_days")
async def tool_get_active_students_last_7_days() -> int:
    """Get count of students active in the last 7 days."""
    return await student_service.get_active_students_last_7_days()


@tool("get_cafeteria_timings")
def tool_get_cafeteria_timings() -> Dict[str, Any]:
    """Get cafeteria operating hours."""
    return {"cafeteria_timings": "Mon-Fri 8am-8pm, Sat 9am-5pm, Sun closed"}


@tool("get_library_hours")
def tool_get_library_hours() -> Dict[str, Any]:
    """Get library operating hours."""
    return {"library_hours": "Mon-Sun 8am-10pm"}


@tool("get_event_schedule")
def tool_get_event_schedule() -> Dict[str, Any]:
    """Get upcoming campus events schedule."""
    return {"events": [
        {"title": "Orientation", "date": "2025-09-25"},
        {"title": "Hackathon Finals", "date": "2025-10-05"},
    ]}


@tool("send_email")
def tool_send_email(student_id: str, message: str) -> Dict[str, Any]:
    """Send email notification to a student."""
    # Mock email send
    return {"status": "queued", "student_id": student_id, "message": message}


@tool("search_uaf_knowledge_and_web")
async def tool_search_uaf_knowledge_and_web(query: str) -> Dict[str, Any]:
    """Search UAF university knowledge base and web for information not related to student database operations."""
    try:
        # Import the RAG agent
        from agent.ragagent import UAFAgentTool
        
        # Initialize the RAG agent
        rag_agent = UAFAgentTool()
        
        # Generate response using RAG agent
        response = rag_agent.generate_response_for_query(query)
        
        return {
            "query": query,
            "response": response,
            "source": "UAF Knowledge Base + Web Search"
        }
        
    except Exception as e:
        # Fallback to basic web search if RAG agent fails
        try:
            from agent.ragagent import UAFWebSearchTool
            web_search = UAFWebSearchTool()
            results = web_search.search(query, max_results=3)
            
            if results and results[0].get("title") != "Search Error":
                web_summary = "Here's what I found on the web:\n\n"
                for result in results:
                    web_summary += f"**{result['title']}**\n{result['snippet']}\n\n"
                return {
                    "query": query,
                    "response": web_summary,
                    "source": "Web Search Only"
                }
            else:
                return {
                    "query": query,
                    "response": f"I couldn't find specific information about '{query}'. This might be outside my knowledge area.",
                    "source": "No Results"
                }
        except Exception as fallback_error:
            return {
                "query": query,
                "response": f"I'm sorry, I couldn't search for information about '{query}' at the moment. Error: {str(e)}",
                "source": "Error",
                "error": str(fallback_error)
            }


def send_admin_notification(action: str, student_data: dict) -> Dict[str, Any]:
    """Send real email notification to admin for student CRUD operations."""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from settings import get_settings
        settings = get_settings()
        
        # Format the email message
        if action == "created":
            subject = f"🎓 New Student Added: {student_data.get('name')}"
            message = f"""
A new student has been added to the system:

📝 Student Details:
- Name: {student_data.get('name')}
- ID: {student_data.get('student_id')}
- Department: {student_data.get('department')}
- Email: {student_data.get('email')}
- Added: {student_data.get('created_at')}

🏛️ Campus Admin System
            """
        elif action == "updated":
            subject = f"📝 Student Updated: {student_data.get('name')}"
            message = f"""
A student record has been updated:

📝 Student Details:
- Name: {student_data.get('name')}
- ID: {student_data.get('student_id')}
- Department: {student_data.get('department')}
- Email: {student_data.get('email')}
- Updated: {student_data.get('updated_at')}

🏛️ Campus Admin System
            """
        elif action == "deleted":
            subject = f"🗑️ Student Deleted: {student_data.get('student_id')}"
            message = f"""
A student record has been deleted:

📝 Deleted Student:
- Student ID: {student_data.get('student_id')}
- Deleted at: {student_data.get('deleted_at')}

🏛️ Campus Admin System
            """
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = settings.email_from
        msg['To'] = settings.smtp_username
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        # Send email via SMTP
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
        
        print(f"✅ EMAIL SENT: {subject} to {settings.smtp_username}")
        
        return {
            "status": "sent",
            "to": settings.smtp_username,
            "subject": subject,
            "action": action
        }
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        # Fallback to console log
        print(f"📧 EMAIL NOTIFICATION (FALLBACK):")
        print(f"To: {settings.smtp_username}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print("-" * 50)
        return {"status": "failed", "error": str(e)}


@tool("get_campus_analytics_summary")
async def tool_get_campus_analytics_summary() -> Dict[str, Any]:
    """Get a comprehensive, user-friendly campus analytics summary."""
    try:
        print("📊 DEBUG: Starting campus analytics summary...")
        
        total = await student_service.get_total_students()
        print(f"👥 DEBUG: Total students: {total}")
        
        by_dept = await student_service.get_students_by_department()
        print(f"🏛️ DEBUG: Departments: {len(by_dept)} found")
        
        recent = await student_service.get_recent_onboarded_students(3)
        print(f"👋 DEBUG: Recent students: {len(recent)} found")
        
        active = await student_service.get_active_students_last_7_days()
        print(f"⚡ DEBUG: Active students: {active}")
        
        # Calculate percentages and insights
        active_percentage = round((active / total * 100) if total > 0 else 0, 1)
        
        result = {
            "total_students": total,
            "active_last_7_days": active,
            "active_percentage": active_percentage,
            "department_breakdown": by_dept[:3],  # Top 3 departments
            "total_departments": len(by_dept),
            "recent_students": [{"name": s.name, "department": s.department} for s in recent],
            "insights": {
                "most_popular_dept": by_dept[0]["department"] if by_dept else "None",
                "engagement_level": "High" if active_percentage > 70 else "Medium" if active_percentage > 40 else "Low"
            }
        }
        
        print(f"✅ DEBUG: Analytics summary completed: {result}")
        return result
        
    except Exception as e:
        error_msg = f"Failed to get analytics summary: {str(e)}"
        print(f"💥 DEBUG: Analytics error: {error_msg}")
        return {"error": error_msg}


