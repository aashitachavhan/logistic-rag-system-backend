from fastapi import FastAPI
from app.routes import upload, chat

app = FastAPI(title="Logistics RAG System")

app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Logistics RAG API Running"}
