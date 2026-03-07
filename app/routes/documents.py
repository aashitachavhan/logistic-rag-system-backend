from fastapi import APIRouter
from app.database.mongo import get_all_documents
from app.models.schemas import DocumentListResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/", response_model=DocumentListResponse)
def get_documents():
    """
    Retrieve all uploaded documents with their metadata.
    
    Returns:
        DocumentListResponse: List of documents and total count
    """
    documents = get_all_documents()
    return DocumentListResponse(
        count=len(documents),
        documents=documents
    )
