# Logistics RAG System - Backend

## 🎯 Key Highlights
- Built an end-to-end Retrieval-Augmented Generation (RAG) system for logistics documents  
- Implemented semantic search using vector embeddings and ChromaDB  
- Integrated LLM APIs to generate context-aware responses with page-level citations  

---

## 📌 Project Overview
A FastAPI-based backend service for a Retrieval-Augmented Generation (RAG) system designed for logistics and supply chain documents. Users can upload PDFs and query them through a chat interface powered by AI.

---

## ⚙️ Tech Stack
**Backend:** FastAPI, ChromaDB, MongoDB, Google Gemini API, Sentence-Transformers  
**Frontend:** Next.js, Tailwind CSS  

---

## 🔗 Repositories
- 🔹 Frontend: https://github.com/aashitachavhan/logistic-rag-system-newfrontend
- 🔹 Backend: https://github.com/aashitachavhan/logistic-rag-system-backend

---

## 🚀 Features
- PDF upload & processing  
- Semantic chunking and embedding generation  
- Vector similarity search for relevant context retrieval  
- Chat-based querying using LLM APIs  
- Page-level citations and source tracking  
- RESTful API for frontend integration  

---

## 🔧 Setup

```bash
git clone <your-backend-repo-url>
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
MONGODB_URL=your_mongodb_url
```

---

## 🚀 Run the Application

```bash
uvicorn app.main:app --reload
```

API runs at:  
👉 http://localhost:8000  

---

## 📚 API Documentation
- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

---

## 🏗️ Architecture Highlights
- Modular backend with services for RAG pipeline, embeddings, and vector search  
- FastAPI-based REST architecture for scalable integration  
- Efficient document processing with semantic chunking  

---

