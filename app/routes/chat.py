from fastapi import APIRouter
from app.services.rag_pipeline import generate_answer
from app.models.schemas import ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
def chat(request: ChatRequest):
    """
    Chat endpoint for asking questions about uploaded logistics documents.
    
    Uses RAG (Retrieval-Augmented Generation) to retrieve relevant
    document chunks and generate comprehensive answers.
    
    Args:
        request (ChatRequest): Contains the user's question and document filter.
    
    Returns:
        dict: Contains the generated answer.
    """
    answer = generate_answer(request.question, request.document)
    return {"answer": answer}
