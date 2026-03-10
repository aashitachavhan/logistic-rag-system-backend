from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.rag_pipeline import generate_answer
from app.models.schemas import ChatRequest, ChatResponse, ChatSession, Message
from app.database.mongo import (
    create_chat_session, get_all_chat_sessions, get_chat_session_by_id,
    update_chat_session, delete_chat_session
)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint for asking questions about uploaded logistics documents.
    
    Uses RAG (Retrieval-Augmented Generation) to retrieve relevant
    document chunks and generate comprehensive answers.
    
    Args:
        request (ChatRequest): Contains the user's question and document filter.
    
    Returns:
        ChatResponse: Contains the generated answer and sources.
    """
    result = generate_answer(request.question, request.document)
    return ChatResponse(answer=result["answer"], sources=result["sources"])


@router.post("/create-session")
def create_session(request: dict = {}):
    """
    Create a new chat session.
    
    Args:
        request: Optional dict with session_title
    
    Returns:
        dict: Session ID.
    """
    session_data = {
        "session_title": request.get("session_title", f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"),
        "created_at": datetime.utcnow(),
        "messages": []
    }
    session_id = create_chat_session(session_data)
    if not session_id:
        raise HTTPException(status_code=500, detail="Failed to create session")
    return {"session_id": session_id}


@router.get("/sessions")
def list_sessions():
    """
    List all chat sessions.
    
    Returns:
        list: List of sessions.
    """
    return get_all_chat_sessions()


@router.get("/session/{session_id}")
def get_session(session_id: str):
    """
    Get a chat session by ID.
    
    Args:
        session_id (str): The session ID.
    
    Returns:
        ChatSession: The session data.
    """
    session = get_chat_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/{session_id}")
def chat_with_session(session_id: str, request: ChatRequest):
    """
    Send a message in an existing chat session.
    
    Args:
        session_id (str): The session ID.
        request (ChatRequest): The chat request.
    
    Returns:
        ChatResponse: The response.
    """
    session = get_chat_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Generate answer
    result = generate_answer(request.question, request.document)
    
    # Add user message
    user_message = Message(role="user", content=request.question)
    session["messages"].append(user_message.dict())
    
    # Add assistant message
    assistant_message = Message(role="assistant", content=result["answer"], sources=result["sources"])
    session["messages"].append(assistant_message.dict())
    
    # Update session
    update_data = {"messages": session["messages"]}
    if not update_chat_session(session_id, update_data):
        raise HTTPException(status_code=500, detail="Failed to update session")
    
    return ChatResponse(answer=result["answer"], sources=result["sources"])


@router.delete("/session/{session_id}")
def delete_session(session_id: str):
    """
    Delete a chat session.
    
    Args:
        session_id (str): The session ID.
    
    Returns:
        dict: Success message.
    """
    if not delete_chat_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted"}
