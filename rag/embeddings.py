"""
embeddings.py

Creates Gemini embeddings for text.
"""

from google import genai

from config import GEMINI_API_KEY
from config import EMBEDDING_MODEL


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def create_embedding(text: str) -> list[float]:
    """
    Generate embedding for a text chunk.
    """

    response = client.models.embed_content(

        model=EMBEDDING_MODEL,

        contents=text

    )

    return response.embeddings[0].values


# -------------------------------------
# Test
# -------------------------------------

if __name__ == "__main__":

    vector = create_embedding(
        "Python Developer with LangGraph experience"
    )

    print()

    print(f"Embedding Length : {len(vector)}")

    print()

    print(vector[:10])