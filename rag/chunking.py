"""
chunking.py

Splits resumes into overlapping chunks for better retrieval.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------
# Resume Text Splitter
# ---------------------------------------------

splitter = RecursiveCharacterTextSplitter(

    chunk_size=800,

    chunk_overlap=150,

    separators=[

        "\n\n",

        "\n",

        ". ",

        " ",

        ""

    ]
)


def split_resume(text: str) -> list[dict]:
    """
    Split resume into chunks with metadata.
    """

    chunks = splitter.split_text(text)

    return [

        {

            "chunk_id": i,

            "text": chunk

        }

        for i, chunk in enumerate(chunks, start=1)

    ]


# ---------------------------------------------
# Test
# ---------------------------------------------

if __name__ == "__main__":

    from rag.loader import load_all_resumes

    resumes = load_all_resumes()

    chunks = split_resume(resumes[0]["text"])

    print("=" * 60)

    print(f"Chunks Created : {len(chunks)}")

    print("=" * 60)

    for chunk in chunks:
        print(f"\nChunk {chunk['chunk_id']}")

        print("-" * 50)

        print(chunk["text"][:400])