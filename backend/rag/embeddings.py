import os
import time
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# =====================================================
# CONFIGURATION
# =====================================================

load_dotenv()

PDF_FOLDER = Path("rag/documents")
VECTOR_FOLDER = Path("rag/vector_store")

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# =====================================================
# LOAD PDFS
# =====================================================

def load_documents():

    documents = []

    pdf_files = list(PDF_FOLDER.glob("*.pdf"))

    print(f"\nFound {len(pdf_files)} PDF files\n")

    skipped = 0

    for i, pdf in enumerate(pdf_files, start=1):

        try:

            print(f"[{i}/{len(pdf_files)}] Loading : {pdf.name}")

            loader = PyPDFLoader(str(pdf))

            pages = loader.load()

            # Save PDF name as metadata
            for page in pages:
                page.metadata["source_file"] = pdf.name

            documents.extend(pages)

        except Exception as e:

            skipped += 1

            print(f"❌ Skipped {pdf.name}")

            print(e)

    print("\n-------------------------------------")

    print(f"Loaded Pages : {len(documents)}")

    print(f"Skipped PDFs : {skipped}")

    print("-------------------------------------\n")

    return documents


# =====================================================
# SPLIT DOCUMENTS
# =====================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP

    )

    chunks = splitter.split_documents(documents)

    print(f"Documents Loaded = {len(documents)}")
    print(f"Chunks Created = {len(chunks)}")
    print(f"Total Chunks : {len(chunks)}\n")

    return chunks


# =====================================================
# CREATE VECTOR DATABASE
# =====================================================

def create_vector_db(chunks):

    embeddings = HuggingFaceEmbeddings(

        model_name=EMBEDDING_MODEL

    )
    print("Creating CHroma ...")
    
    print(chunks[:2])

    vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="rag/chroma_db"
)

    print("\n✅ Chroma Database Saved Successfully")


# =====================================================
# MAIN
# =====================================================

def main():

    start = time.time()

    print("=" * 60)
    print("KERALA FARMING RAG")
    print("=" * 60)

    documents = load_documents()

    chunks = split_documents(documents)

    create_vector_db(chunks)

    end = time.time()

    print("\n-------------------------------------")
    print(f"Completed in {(end-start)/60:.2f} minutes")
    print("-------------------------------------")


if __name__ == "__main__":

    main()
