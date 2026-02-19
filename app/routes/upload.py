from fastapi import APIRouter, UploadFile, File
from app.services.pdf_loader import load_pdf
from app.services.chunking import chunk_text
from app.services.vector_store import store_chunks

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    text = await load_pdf(file)
    chunks = chunk_text(text)
    store_chunks(chunks)
    return {"message": "Document processed successfully"}
