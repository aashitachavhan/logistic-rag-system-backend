from fastapi import APIRouter, HTTPException
from app.database.mongo import get_all_documents, delete_document_metadata
from app.services.vector_store import delete_chunks_by_source
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


@router.delete("/{filename}")
def delete_document(filename: str):
    """
    Delete a document by filename.
    
    Removes the document metadata from MongoDB and embeddings from the vector store.
    
    Args:
        filename (str): The filename of the document to delete.
    
    Returns:
        dict: Success message.
    """
    # Delete metadata from MongoDB
    metadata_deleted = delete_document_metadata(filename)
    
    # Delete embeddings from vector store
    delete_chunks_by_source(filename)
    
    if not metadata_deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {"message": "Document deleted successfully"}
