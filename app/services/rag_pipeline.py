from google import genai
from app.services.vector_store import query_chunks
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an AI assistant specialized in logistics documents.

Your responsibilities:
1. Answer questions based ONLY on the provided document context.
2. Always provide full sentence responses.
3. Do not return only numbers, codes, or fragments.
4. Explain information in a clear, professional, and readable way.
5. If the answer is not found in the documents, clearly state: "I could not find this information in the provided documents."

Example good responses:
- Instead of "MSCU1234567" → "The container number mentioned in the document is MSCU1234567."
- Instead of "20ft" → "The document specifies that this is a 20-foot standard container."
- Instead of "Shanghai" → "According to the shipping document, the port of origin is Shanghai."

Always prioritize clarity and completeness in your responses."""


def generate_answer(question):
    """
    Generate an answer using RAG (Retrieval-Augmented Generation).
    
    Retrieves relevant document chunks and uses Gemini to generate
    a comprehensive, well-formatted response.
    
    Args:
        question (str): The user's question.
    
    Returns:
        str: The generated answer.
    """
    context_chunks = query_chunks(question)
    context = "\n\n".join(context_chunks)

    prompt = f"""{SYSTEM_PROMPT}

Context from documents:
{context}

User Question:
{question}

Please provide a clear, complete answer based on the context above."""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
