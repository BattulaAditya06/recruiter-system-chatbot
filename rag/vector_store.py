"""
build_store.py

Builds the Chroma Vector Database from resumes.
"""

import chromadb

from config import CHROMA_DB_PATH
from utils.logger import logger

from rag.loader import load_all_resumes
from rag.chunking import split_resume
from rag.embeddings import create_embedding


# -------------------------------------------------------
# Chroma Client
# -------------------------------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)

collection = client.get_or_create_collection(
    name="resume_store"
)


# -------------------------------------------------------
# Build Vector Store
# -------------------------------------------------------

def build_vector_store():

    resumes = load_all_resumes()

    total_chunks = 0

    for resume in resumes:

        candidate = resume["candidate_name"]

        filename = resume["resume_file"]

        chunks = split_resume(
            resume["text"]
        )

        for chunk in chunks:

            embedding = create_embedding(
                chunk["text"]
            )

            doc_id = f"{candidate}_{chunk['chunk_id']}"

            collection.add(

                ids=[doc_id],

                documents=[chunk["text"]],

                embeddings=[embedding],

                metadatas=[

                    {

                        "candidate_name": candidate,

                        "resume_file": filename,

                        "chunk_id": chunk["chunk_id"]

                    }

                ]

            )

            total_chunks += 1

    logger.info(
        f"{total_chunks} chunks stored."
    )


# -------------------------------------------------------
# Test
# -------------------------------------------------------

if __name__ == "__main__":

    build_vector_store()

    print()

    print("=" * 60)

    print("Vector Store Built Successfully")

    print("=" * 60)