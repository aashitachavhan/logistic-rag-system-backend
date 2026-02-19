from google import genai
from app.services.vector_store import query_chunks
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_answer(question):
    context_chunks = query_chunks(question)
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a logistics document assistant.

Use ONLY the context below to answer.
If answer is not found, say:
"Answer not found in provided documents."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
