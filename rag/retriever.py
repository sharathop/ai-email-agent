from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"

# -----------------------------
# Chroma
# -----------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_collection(
    name="career_assistant"
)

# -----------------------------
# Embedding Model
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# Retrieval
# -----------------------------

def retrieve(query, category=None, project=None, k=5):

    embedding = model.encode(query).tolist()

    where = {}

    if category:
        where["document_type"] = category

    if project:
        where["project_name"] = project

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        where=where if where else None,
    )

    return results