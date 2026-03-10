from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DocumentMetadata(BaseModel):
    """Schema for document metadata stored in MongoDB."""
    filename: str
    upload_time: datetime
    is_logistics_document: bool
    extracted_preview: str


class DocumentResponse(BaseModel):
    """Response schema for upload endpoint."""
    filename: str
    is_logistics_document: bool
    message: str


class DocumentListResponse(BaseModel):
    """Response schema for documents list endpoint."""
    count: int
    documents: list


class ChatRequest(BaseModel):
    """Schema for chat endpoint request."""
    question: str
    document: Optional[str] = None


class Source(BaseModel):
    """Schema for source citation."""
    document: str
    page: int


class ChatResponse(BaseModel):
    """Schema for chat endpoint response."""
    answer: str
    sources: List[Source]


class Message(BaseModel):
    """Schema for a chat message."""
    role: str  # "user" or "assistant"
    content: str
    sources: Optional[List[Source]] = None


class ChatSession(BaseModel):
    """Schema for a chat session."""
    id: Optional[str] = None
    session_title: str
    created_at: datetime
    messages: List[Message]
