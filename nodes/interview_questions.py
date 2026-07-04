"""
interview_questions.py
"""

from google import genai

from config import GEMINI_API_KEY, MODEL_NAME

from schemas.interview_schema import InterviewSchema

client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are a Senior Technical Interviewer.

Generate personalized interview questions.

Rules

Use only the supplied Job Description and Candidate Evaluation.

Generate

3 Technical Questions

2 Project Questions

2 Behavioural Questions

The questions must evaluate:

- Missing mandatory skills
- Candidate strengths
- Candidate projects

Do not ask generic questions.

Return only structured JSON.
"""


def generate_interview_questions(jd, screening):

    prompt = f"""
JOB DESCRIPTION

{jd.model_dump_json(indent=2)}

Candidate Evaluation

{screening}
"""

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=[
            SYSTEM_PROMPT,
            prompt
        ],

        config={

            "response_schema": InterviewSchema,

            "response_mime_type": "application/json"

        }

    )

    return response.parsed

if __name__ == "__main__":

    from rag.loader import load_job_description
    from nodes.parse_jd import parse_job_description
    from rag.retriever import retrieve_candidate_evidence
    from nodes.screen_candidates import screen_candidate

    jd_text = load_job_description("ai_engineer.txt")

    jd = parse_job_description(jd_text)

    candidates = retrieve_candidate_evidence(jd.description)

    best_candidate = screen_candidate(jd, candidates[0])

    questions = generate_interview_questions(
        jd,
        best_candidate
    )

    print("=" * 70)
    print("INTERVIEW QUESTIONS")
    print("=" * 70)

    print("\nTechnical Questions")

    for q in questions.technical_questions:
        print("-", q.question)

    print("\nProject Questions")

    for q in questions.project_questions:
        print("-", q.question)

    print("\nBehavioural Questions")

    for q in questions.behavioral_questions:
        print("-", q.question)