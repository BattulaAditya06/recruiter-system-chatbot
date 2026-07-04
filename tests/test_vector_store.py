import chromadb

from config import CHROMA_DB_PATH

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)

collection = client.get_collection("resume_store")

print("=" * 50)
print("Collection Name :", collection.name)
print("Total Chunks    :", collection.count())
print("=" * 50)