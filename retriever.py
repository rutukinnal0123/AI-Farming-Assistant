from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================================
# Embedding Model
# ==========================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# ==========================================================
# Chroma Database
# ==========================================================

CHROMA_DB_PATH = Path(__file__).parent / "chroma_db"

vector_db = Chroma(
    persist_directory=str(CHROMA_DB_PATH),
    embedding_function=embedding_model
)

print("✅ ChromaDB Loaded Successfully")


# ==========================================================
# Retrieve Documents
# ==========================================================

def retrieve_documents(
    question: str,
    k: int = 5,
    threshold: float = 0.55
):

    results = vector_db.similarity_search_with_relevance_scores(
        question,
        k=k
    )

    good_docs = []

    for doc, score in results:

        if score >= threshold:

            good_docs.append(doc)

    return good_docs

