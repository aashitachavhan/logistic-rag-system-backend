from sentence_transformers import SentenceTransformer

# Load free local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    embedding = model.encode(text)
    return embedding.tolist()
