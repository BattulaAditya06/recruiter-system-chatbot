"""
parse_jd.py

Converts a raw Job Description into a structured JobSchema.
"""

from google import genai

from config import GEMINI_API_KEY
from config import MODEL_NAME

from schemas.job_schema import JobSchema


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_PROMPT = """
You are an expert HR recruitment assistant.

Extract the provided Job Description into the JobSchema exactly.

Rules:
1. Do NOT invent information.
2. If a field is missing, leave it empty or null.
3. Separate mandatory skills and preferred skills correctly.
4. Extract responsibilities as a list.
5. Generate keywords from the important technologies and skills mentioned.
6. Preserve the original job description in the description field.
Return only the structured response.
"""

def parse_job_description(jd_text: str):

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=[
            SYSTEM_PROMPT,
            jd_text
        ],

        config={

            "response_mime_type":"application/json",

            "response_schema":JobSchema

        }

    )

    return response.parsed


if __name__ == "__main__":

    from rag.loader import load_job_description

    jd = load_job_description(
        "ai_engineer.txt"
    )

    parsed = parse_job_description(jd)

    print(parsed)