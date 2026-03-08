import chromadb
from app.services.embeddings import get_embedding

client = chromadb.Client()
collection = client.get_or_create_collection("logistics_docs")

def store_chunks(chunks, source_filename):
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": source_filename}],
            ids=[f"{source_filename}_{i}"]
        )

def query_chunks(query, source_filter=None):
    query_embedding = get_embedding(query)
    if source_filter:
        results = collection.query(
            query_embeddings=[query_embedding],
            where={"source": source_filter},
            n_results=3
        )
    else:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
    return results["documents"][0] if results["documents"] else []

def delete_chunks_by_source(source_filename):
    try:
        collection.delete(where={"source": source_filename})
    except Exception as e:
        print(f"Error deleting chunks for {source_filename}: {e}")
