"""
interview_questions.py

Generates personalized interview questions.
"""

from google import genai

from config import GEMINI_API_KEY, MODEL_NAME
from schemas.interview_schema import InterviewSchema

client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are a Senior Technical Interviewer.

Generate personalized interview questions.

Rules

Use ONLY the supplied Job Description and Candidate Evaluation.

Generate:

- 3 Technical Questions
- 2 Project Questions
- 2 Behavioral Questions

The questions should evaluate:

• Missing mandatory skills
• Candidate strengths
• Candidate projects

Return structured JSON only.
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

    result = response.parsed

    return {

        "candidate_name": screening["candidate_name"],

        "technical_questions": [
            q.question for q in result.technical_questions
        ],

        "project_questions": [
            q.question for q in result.project_questions
        ],

        "behavioral_questions": [
            q.question for q in result.behavioral_questions
        ]

    }


def save_questions(interview_results,
                   filename="Interview_Questions.txt"):

    with open(filename, "w", encoding="utf-8") as file:

        file.write("=" * 80 + "\n")
        file.write("HIREPILOT AI - INTERVIEW QUESTIONS\n")
        file.write("=" * 80 + "\n\n")

        for candidate in interview_results:

            file.write(
                f"Candidate : {candidate['candidate_name']}\n"
            )

            file.write("-" * 80 + "\n")

            file.write("\nTechnical Questions\n")

            for q in candidate["technical_questions"]:
                file.write(f"• {q}\n")

            file.write("\nProject Questions\n")

            for q in candidate["project_questions"]:
                file.write(f"• {q}\n")

            file.write("\nBehavioral Questions\n")

            for q in candidate["behavioral_questions"]:
                file.write(f"• {q}\n")

            file.write("\n\n")

    print(f"✓ Interview Questions saved to {filename}")


if __name__ == "__main__":

    from rag.loader import load_job_description
    from nodes.parse_jd import parse_job_description
    from rag.retriever import retrieve_candidate_evidence
    from nodes.screen_candidates import screen_candidate

    jd_text = load_job_description("ai_engineer.txt")

    jd = parse_job_description(jd_text)

    candidates = retrieve_candidate_evidence(jd.description)

    screened = screen_candidate(jd, candidates[0])

    questions = generate_interview_questions(
        jd,
        screened
    )

    print("=" * 70)
    print("INTERVIEW QUESTIONS")
    print("=" * 70)

    print("\nTechnical Questions")

    for q in questions["technical_questions"]:
        print("-", q)

    print("\nProject Questions")

    for q in questions["project_questions"]:
        print("-", q)

    print("\nBehavioral Questions")

    for q in questions["behavioral_questions"]:
        print("-", q)

    save_questions([questions])