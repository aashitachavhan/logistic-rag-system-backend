from fastapi import APIRouter
from app.services.rag_pipeline import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
def chat(query: dict):
    answer = generate_answer(query["question"])
    return {"answer": answer}
