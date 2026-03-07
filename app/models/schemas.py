from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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
