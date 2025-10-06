from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from settings import get_settings
from agent.tools import (
    tool_add_student,
    tool_get_student,
    tool_update_student,
    tool_delete_student,
    tool_list_students,
    tool_get_total_students,
    tool_get_students_by_department,
    tool_get_students_count_by_specific_department,
    tool_get_recent_onboarded_students,
    tool_get_active_students_last_7_days,
    tool_get_cafeteria_timings,
    tool_get_library_hours,
    tool_get_event_schedule,
    tool_send_email,
    tool_get_campus_analytics_summary,
    tool_search_uaf_knowledge_and_web,
)


SYSTEM_MESSAGE = SystemMessage(content=(
    "You are a friendly AI Campus Admin Assistant with access to multiple capabilities:\n\n"
    "📊 STUDENT DATABASE OPERATIONS:\n"
    "- Use student management tools for CRUD operations, analytics, and student data queries\n"
    "- Always use tools to get real data when asked about students, analytics, or campus info\n\n"
    "🏛️ UAF UNIVERSITY KNOWLEDGE:\n"
    "- For questions about UAF University, academics, admissions, faculty, or general university info\n"
    "- Use the search_uaf_knowledge_and_web tool for UAF-related queries\n\n"
    "🌐 WEB SEARCH:\n"
    "- For general questions not related to student database or UAF university\n"
    "- Use web search capabilities for current information\n\n"
    "RESPONSE STYLE:\n"
    "- Use conversational, friendly language\n"
    "- Present data in easy-to-read formats\n"
    "- Add helpful context and insights\n"
    "- Use emojis to make responses more engaging\n"
    "- Offer follow-up suggestions\n"
    "- Keep responses concise but informative\n\n"
    "Choose the appropriate tool based on the user's query type."
))


def build_agent():
    settings = get_settings()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=settings.openai_api_key)
    tools = [
        tool_add_student,
        tool_get_student,
        tool_update_student,
        tool_delete_student,
        tool_list_students,
        tool_get_total_students,
        tool_get_students_by_department,
        tool_get_students_count_by_specific_department,
        tool_get_recent_onboarded_students,
        tool_get_active_students_last_7_days,
        tool_get_cafeteria_timings,
        tool_get_library_hours,
        tool_get_event_schedule,
        tool_send_email,
        tool_get_campus_analytics_summary,
        tool_search_uaf_knowledge_and_web,
    ]
    memory = MemorySaver()
    agent = create_react_agent(llm, tools, checkpointer=memory)
    return agent


