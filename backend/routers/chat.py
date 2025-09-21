from typing import AsyncGenerator, Optional
import uuid
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from sse_starlette.sse import EventSourceResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas import ChatRequest, VoiceChatRequest, VoiceUploadRequest, ChatMessage, UserChatRequest, ChatHistoryResponse
from agent.graph import build_agent, SYSTEM_MESSAGE
from services.voice import get_voice_service
from services.chat_history import save_chat_entry, get_user_chat_history, get_user_session_history, delete_user_chat_history, get_recent_users_with_chats, get_chat_statistics
from services.auth import get_current_active_user
from models.user import UserInDB
from db import get_database


router = APIRouter()
graph = build_agent()


@router.post("/chat/authenticated")
async def authenticated_chat(
    req: ChatRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Authenticated chat endpoint - uses the logged-in user's ID for chat history
    """
    try:
        config = {"configurable": {"thread_id": current_user.id}}
        messages = [SYSTEM_MESSAGE] + [m.model_dump() for m in req.messages]
        result = await graph.ainvoke({"messages": messages}, config)
        last = result["messages"][-1]
        content = getattr(last, "content", last)
        
        # Get user's last message for history
        user_message = req.messages[-1].content if req.messages else ""
        
        # Save to chat history using authenticated user ID
        session_id = str(uuid.uuid4())
        await save_chat_entry(
            user_id=current_user.id,
            session_id=session_id,
            user_message=user_message,
            ai_response=content
        )
        
        return {
            "messages": [content],
            "text_response": content,
            "session_id": session_id,
            "user_id": current_user.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in authenticated chat: {str(e)}")


@router.post("/chat")
async def universal_chat(req: UserChatRequest):
    """
    Universal chat endpoint - supports text input, returns text response
    Saves chat history to MongoDB (last 10 chats per user)
    Frontend can then use /text-to-speech for voice playback if needed
    """
    try:
        config = {"configurable": {"thread_id": req.user_id}}
        messages = [SYSTEM_MESSAGE] + [m.model_dump() for m in req.messages]
        result = await graph.ainvoke({"messages": messages}, config)
        last = result["messages"][-1]
        content = getattr(last, "content", last)
        
        # Get user's last message for history
        user_message = req.messages[-1].content if req.messages else ""
        
        # Save to chat history (without audio data)
        session_id = str(uuid.uuid4())
        await save_chat_entry(
            user_id=req.user_id,
            session_id=session_id,
            user_message=user_message,
            ai_response=content
        )
        
        return {
            "messages": [content],
            "text_response": content,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")



async def save_chat_background(user_id: str, user_message: str, ai_response: str):
    """Background task to save chat after streaming completes"""
    try:
        session_id = str(uuid.uuid4())
        await save_chat_entry(
            user_id=user_id,
            session_id=session_id,
            user_message=user_message,
            ai_response=ai_response
        )
    except Exception as e:
        # Log error but don't fail
        print(f"Background save failed: {e}")

@router.get("/stream")
async def authenticated_stream(
    background_tasks: BackgroundTasks,
    messages: str = Query(..., description="JSON encoded messages array"),
    token: Optional[str] = Query(None, description="Bearer token for authentication"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Authenticated streaming endpoint for EventSource (GET requests)
    """
    import json
    from services.auth import get_user_by_username
    from jose import JWTError, jwt
    from settings import get_settings
    
    settings = get_settings()
    
    # Authenticate user from token
    if not token:
        raise HTTPException(status_code=401, detail="Token required")
    
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    current_user = await get_user_by_username(db, username)
    if not current_user or not current_user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    try:
        # Parse messages from query parameter
        parsed_messages = json.loads(messages)
        
        # Filter out invalid messages (missing content) and create ChatMessage objects
        chat_messages = []
        for msg in parsed_messages:
            # Skip messages without content (invalid assistant messages)
            if 'content' not in msg or not msg['content']:
                print(f"Skipping invalid message: {msg}")
                continue
            try:
                chat_messages.append(ChatMessage(**msg))
            except Exception as e:
                print(f"Error creating ChatMessage: {e}, message: {msg}")
                continue
        
        config = {"configurable": {"thread_id": current_user.id}}

        async def event_generator() -> AsyncGenerator[str, None]:
            try:
                # Prepare messages with system prompt
                messages_for_agent = [SYSTEM_MESSAGE] + [m.model_dump() for m in chat_messages]
                
                # Start streaming
                import json
                yield f"{json.dumps({'type': 'start'})}\n\n"
                
                # Stream events from the agent
                response_content = ""
                async for event in graph.astream_events(
                    {"messages": messages_for_agent}, 
                    version="v2", 
                    config=config
                ):
                    # LLM streaming tokens
                    if event["event"] == "on_chat_model_stream":
                        chunk = event["data"].get("chunk")
                        if chunk and hasattr(chunk, "content") and chunk.content:
                            response_content += chunk.content
                            # Send each token with proper JSON formatting
                            yield f"{json.dumps({'content': chunk.content})}\n\n"
                
                # Save to chat history immediately after streaming completes
                if response_content and chat_messages:
                    user_message = chat_messages[-1].content if chat_messages else ""
                    session_id = str(uuid.uuid4())
                    
                    # Try to save immediately - if it fails, don't crash the stream
                    try:
                        saved_entry = await save_chat_entry(
                            user_id=current_user.id,
                            session_id=session_id,
                            user_message=user_message,
                            ai_response=response_content
                        )
                        # Send a success indicator (optional)
                        yield f"{json.dumps({'type': 'saved', 'id': saved_entry.id})}\n\n"
                    except Exception as save_error:
                        # Send error indicator but don't crash
                        yield f"{json.dumps({'type': 'save_error', 'error': str(save_error)})}\n\n"
                
                # End streaming - send completion data first, then close
                yield f"{json.dumps({'type': 'complete'})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': f'❌ Error: {str(e)}'})}\n\n"

        return EventSourceResponse(event_generator())
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid messages format: {str(e)}")


@router.post("/stream")
async def universal_stream(req: UserChatRequest):
    """
    Universal streaming endpoint - supports text input, streams text response
    Saves chat history to MongoDB (last 10 chats per user)
    Frontend can use final response with /text-to-speech for voice playback
    """
    config = {"configurable": {"thread_id": req.user_id}}

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            # Prepare messages with system prompt
            messages = [SYSTEM_MESSAGE] + [m.model_dump() for m in req.messages]
            
            # Start streaming
            yield f"data: {{\"type\": \"start\", \"message\": \"🤖 AI Campus Admin is thinking...\"}}\n\n"
            
            # Stream events from the agent
            response_content = ""
            async for event in graph.astream_events(
                {"messages": messages}, 
                version="v2", 
                config=config
            ):
                # Tool execution events
                if event["event"] == "on_tool_start":
                    tool_name = event.get("name", "unknown")
                    yield f"data: {{\"type\": \"tool_start\", \"tool\": \"{tool_name}\", \"message\": \"🔧 Using {tool_name}...\"}}\n\n"
                
                elif event["event"] == "on_tool_end":
                    tool_name = event.get("name", "unknown")
                    yield f"data: {{\"type\": \"tool_end\", \"tool\": \"{tool_name}\", \"message\": \"✅ {tool_name} completed\"}}\n\n"
                
                # LLM streaming tokens
                elif event["event"] == "on_chat_model_stream":
                    chunk = event["data"].get("chunk")
                    if chunk and hasattr(chunk, "content") and chunk.content:
                        response_content += chunk.content
                        # Escape quotes in content
                        escaped_content = chunk.content.replace('"', '\\"')
                        yield f"data: {{\"type\": \"token\", \"content\": \"{escaped_content}\"}}\n\n"
            
            # Save to chat history before sending final response
            if response_content:
                user_message = req.messages[-1].content if req.messages else ""
                session_id = str(uuid.uuid4())
                
                try:
                    await save_chat_entry(
                        user_id=req.user_id,
                        session_id=session_id,
                        user_message=user_message,
                        ai_response=response_content
                    )
                except Exception as e:
                    print(f"Warning: Failed to save chat history: {e}")
                
                # Send final complete response for voice conversion
                escaped_final = response_content.replace('"', '\\"').replace('\n', '\\n')
                yield f"data: {{\"type\": \"final_response\", \"content\": \"{escaped_final}\", \"session_id\": \"{session_id}\"}}\n\n"
            
            # Final response
            yield f"data: {{\"type\": \"complete\", \"message\": \"✨ Response completed!\"}}\n\n"
            yield f"data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: {{\"type\": \"error\", \"message\": \"❌ Error: {str(e)}\"}}\n\n"
            yield f"data: [DONE]\n\n"

    return EventSourceResponse(event_generator())


@router.post("/voice-to-text")
async def voice_to_text(req: VoiceUploadRequest):
    """
    Convert uploaded voice audio to text
    Frontend: Record voice → Send here → Get text → Send to /chat or /stream
    """
    try:
        voice_service = get_voice_service()
        result = voice_service.speech_to_text(req.audio_data)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "text": result["text"],
            "message": result["message"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")


@router.post("/text-to-speech")
async def text_to_speech(request: dict):
    """
    Convert text to speech audio
    Frontend: Get response from /chat → Send text here → Play audio
    
    Body: {"text": "response text", "voice_id": "optional_voice_id"}
    """
    try:
        text = request.get("text", "")
        voice_id = request.get("voice_id", "JBFqnCBsd6RMkjVDRZzb")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        voice_service = get_voice_service()
        result = voice_service.text_to_speech(text, voice_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "audio_base64": result["audio_base64"],
            "voice_id": result["voice_id"],
            "message": result["message"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")


@router.get("/voices")
async def get_available_voices():
    """
    Get list of available ElevenLabs voices for frontend voice selection
    """
    try:
        voice_service = get_voice_service()
        result = voice_service.get_available_voices()
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching voices: {str(e)}")


@router.get("/history/me")
async def get_my_chat_history(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Get chat history for the authenticated user
    """
    try:
        history = await get_user_chat_history(current_user.id)
        return {
            "user_id": current_user.id,
            "username": current_user.username,
            "total_chats": history.total_chats,
            "chats": [
                {
                    "id": chat.id,
                    "user_id": chat.user_id,
                    "session_id": chat.session_id,
                    "user_message": chat.user_message,
                    "ai_response": chat.ai_response,
                    "timestamp": chat.timestamp.isoformat() if chat.timestamp else None,
                    "created_at": chat.created_at.isoformat() if chat.created_at else None,
                }
                for chat in history.chats
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")


@router.get("/history/{user_id}", response_model=ChatHistoryResponse)
async def get_user_history(user_id: str, limit: int = Query(10, ge=1, le=50)):
    """
    Get chat history for a specific user
    Returns last N chats (default 10, max 50)
    """
    try:
        history = await get_user_chat_history(user_id, limit)
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")


@router.get("/history/{user_id}/session/{session_id}")
async def get_session_history(user_id: str, session_id: str):
    """
    Get all chats for a specific user session
    """
    try:
        chats = await get_user_session_history(user_id, session_id)
        return {
            "user_id": user_id,
            "session_id": session_id,
            "chats": chats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching session history: {str(e)}")


@router.delete("/history/me")
async def delete_my_chat_history(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Delete all chat history for the authenticated user
    """
    try:
        deleted_count = await delete_user_chat_history(current_user.id)
        return {
            "message": f"Deleted {deleted_count} chat entries for user {current_user.username}",
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat history: {str(e)}")


@router.delete("/history/{user_id}")
async def delete_user_history(user_id: str):
    """
    Delete all chat history for a specific user
    """
    try:
        deleted_count = await delete_user_chat_history(user_id)
        return {
            "message": f"Deleted {deleted_count} chat entries for user {user_id}",
            "user_id": user_id,
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat history: {str(e)}")


@router.get("/history/users/recent")
async def get_recent_chat_users(limit: int = Query(20, ge=1, le=100)):
    """
    Get list of users who have recent chat history
    """
    try:
        users = await get_recent_users_with_chats(limit)
        return {
            "recent_users": users,
            "count": len(users)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent users: {str(e)}")


@router.get("/history/statistics")
async def get_chat_stats():
    """
    Get overall chat statistics
    """
    try:
        stats = await get_chat_statistics()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat statistics: {str(e)}")