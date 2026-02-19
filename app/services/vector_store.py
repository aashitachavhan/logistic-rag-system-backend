import chromadb
from app.services.embeddings import get_embedding

client = chromadb.Client()
collection = client.get_or_create_collection("logistics_docs")

def store_chunks(chunks):
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(i)]
        )

def query_chunks(query):
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    return results["documents"][0]
