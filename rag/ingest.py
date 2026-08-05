
import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"
CHROMA_PATH = BASE_DIR / "chroma_db"

# -----------------------------
# Chroma
# -----------------------------
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

try:
    client.delete_collection("career_assistant")
except Exception:
    pass

collection = client.get_or_create_collection("career_assistant")

# -----------------------------
# Embedding Model
# -----------------------------
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded.")

# -----------------------------
# Splitters
# -----------------------------
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header1"),
        ("##", "Header2"),
        ("###", "Header3"),
    ]
)

pdf_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
)

documents = []

# -----------------------------
# Read files
# -----------------------------
for file in KNOWLEDGE_BASE.rglob("*"):

    if not file.is_file():
        continue

    print(f"Reading {file.name}")

    # -------------------------
    # Markdown
    # -------------------------
    if file.suffix.lower() == ".md":

        docs = TextLoader(str(file), encoding="utf-8").load()
        chunks = markdown_splitter.split_text(docs[0].page_content)

        document_type = "general"
        project_name = ""

        if "projects" in file.parts:
            document_type = "project"
            project_name = file.stem
        elif file.stem == "skills":
            document_type = "skills"
        elif file.stem == "education":
            document_type = "education"
        elif file.stem == "profile":
            document_type = "profile"
        elif file.stem == "github":
            document_type = "github"
        elif file.stem == "linkedin":
            document_type = "linkedin"

        for chunk in chunks:

            metadata = {
                "source": file.name,
                "document_type": document_type,
            }

            if project_name:
                metadata["project_name"] = project_name

            for h in ("Header1", "Header2", "Header3"):
                value = chunk.metadata.get(h)
                if value:
                    metadata[h] = str(value)

            if chunk.metadata.get("Header2"):
                metadata["section"] = str(chunk.metadata["Header2"])

            documents.append(
                {
                    "text": chunk.page_content,
                    "metadata": metadata,
                }
            )

    # -------------------------
    # PDF
    # -------------------------
    elif file.suffix.lower() == ".pdf":

        docs = PyPDFLoader(str(file)).load()
        chunks = pdf_splitter.split_documents(docs)

        for chunk in chunks:

            metadata = {
                "source": file.name,
                "document_type": "resume",
            }

            if "page" in chunk.metadata:
                metadata["page"] = int(chunk.metadata["page"])

            documents.append(
                {
                    "text": chunk.page_content,
                    "metadata": metadata,
                }
            )

print(f"Total chunks: {len(documents)}")

texts = [d["text"] for d in documents]

print("Creating embeddings...")
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
).tolist()

metadatas = []
for d in documents:
    clean = {}
    for k, v in d["metadata"].items():
        if v is None:
            continue
        if isinstance(v, (str, int, float, bool)):
            clean[k] = v
        else:
            clean[k] = str(v)
    metadatas.append(clean)

collection.add(
    ids=[str(i) for i in range(len(documents))],
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,
)

print("Knowledge Base Indexed Successfully.")
