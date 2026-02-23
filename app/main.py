from fastapi import FastAPI
from app.routes import upload, chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Logistics RAG System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Logistics RAG API Running"}
