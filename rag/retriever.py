"""
retriever.py

Retrieves the most relevant resume chunks
from the ChromaDB vector store.
"""

import chromadb

from config import CHROMA_DB_PATH, TOP_K
from rag.embeddings import create_embedding


# -------------------------------------------------------
# Connect to ChromaDB
# -------------------------------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)

collection = client.get_collection(
    "resume_store"
)


# -------------------------------------------------------
# Retrieve Candidate Evidence
# -------------------------------------------------------

def retrieve_candidate_evidence(query: str):
    """
    Retrieve the most relevant candidates.

    Returns:
        list[dict]
    """

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    candidate_map = {}

    for doc, meta, distance in zip(
        documents,
        metadatas,
        distances
    ):

        name = meta["candidate_name"]

        if name not in candidate_map:

            candidate_map[name] = {

                "candidate_name": name,

                "resume_file": meta["resume_file"],

                # keep highest similarity
                "similarity_score": round(1 - distance, 4),

                "evidence": []

            }

        else:

            similarity = round(1 - distance, 4)

            if similarity > candidate_map[name]["similarity_score"]:

                candidate_map[name]["similarity_score"] = similarity

        candidate_map[name]["evidence"].append(doc)

    candidates = sorted(

        candidate_map.values(),

        key=lambda x: x["similarity_score"],

        reverse=True

    )

    return candidates


# -------------------------------------------------------
# Test
# -------------------------------------------------------

if __name__ == "__main__":

    query = """
    Looking for a Python Developer
    with Java,
    SQL,
    Git,
    Machine Learning,
    OOP,
    Problem Solving.
    """

    retrieved = retrieve_candidate_evidence(query)

    print("=" * 70)
    print("Retrieved Candidates")
    print("=" * 70)

    for i, candidate in enumerate(retrieved, start=1):

        print(f"\nCandidate {i}")
        print("-" * 60)

        print("Name       :", candidate["candidate_name"])
        print("Similarity :", candidate["similarity_score"])

        print("\nEvidence:")

        for j, evidence in enumerate(candidate["evidence"], start=1):

            print(f"\nChunk {j}")

            print("-" * 40)

            print(evidence[:300])

        print("\n" + "=" * 70)