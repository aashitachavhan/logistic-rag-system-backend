from fastapi import APIRouter, UploadFile, File
from datetime import datetime
from app.services.pdf_loader import extract_first_page_text_from_bytes, load_pdf_from_bytes
from app.services.chunking import chunk_text
from app.services.vector_store import store_chunks
from app.services.logistics_detector import detect_logistics_document, extract_preview
from app.database.mongo import store_document_metadata
from app.models.schemas import DocumentResponse

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/", response_model=DocumentResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF document and process it for the RAG system.
    
    - Extracts text from the document
    - Detects if it's a logistics document
    - Stores metadata in MongoDB
    - Chunks and embeds the text for ChromaDB
    
    Returns:
        DocumentResponse: Status and detection results
    """
    try:
        # Read file bytes once
        file_bytes = await file.read()
        
        if not file_bytes:
            return DocumentResponse(
                filename=file.filename,
                is_logistics_document=False,
                message="Error: Empty file. Please upload a valid PDF."
            )
        
        # Extract text from first page for logistics detection
        first_page_text = await extract_first_page_text_from_bytes(file_bytes)
        
        # Detect if document is logistics-related
        is_logistics = detect_logistics_document(first_page_text)
        
        # Extract full text for chunking and embedding
        text = await load_pdf_from_bytes(file_bytes)
        
        # Extract preview for metadata storage
        preview = extract_preview(text)
        
        # Store document metadata in MongoDB
        document_metadata = {
            "filename": file.filename,
            "upload_time": datetime.utcnow(),
            "is_logistics_document": is_logistics,
            "extracted_preview": preview
        }
        store_document_metadata(document_metadata)
        
        # Process document for RAG pipeline
        chunks = chunk_text(text)
        store_chunks(chunks)
        
        # Prepare response message
        if is_logistics:
            message = "Logistics document detected"
        else:
            message = "This might not be a logistics document"
        
        return DocumentResponse(
            filename=file.filename,
            is_logistics_document=is_logistics,
            message=message
        )
    
    except Exception as e:
        return DocumentResponse(
            filename=file.filename,
            is_logistics_document=False,
            message=f"Error processing file: {str(e)}"
        )
