"""
screen_candidates.py

Evaluates retrieved candidates against the Job Description.
"""

from google import genai

from config import GEMINI_API_KEY
from config import MODEL_NAME

from schemas.job_schema import JobSchema
from schemas.screening_schema import ScreeningSchema

client = genai.Client(
    api_key=GEMINI_API_KEY
)

SYSTEM_PROMPT = """
You are a Senior Technical Recruiter.

Evaluate ONE candidate against ONE Job Description.

Rules

1. Use ONLY the supplied resume evidence.

2. Never invent skills.

3. Compare skills semantically.

Examples

DSA == Data Structures and Algorithms

OOP == Object Oriented Programming

ML == Machine Learning

4. Do not split one skill into multiple skills.

5. First evaluate mandatory skills.

6. Then evaluate preferred skills.

7. Then evaluate projects.

8. Then education.

Decision Rules

SHORTLIST

Mandatory Match >=80%

No major missing skills

----------------------------------

HOLD

Mandatory Match 50-79%

Candidate can be trained

----------------------------------

REJECT

Mandatory Match below 50%

----------------------------------

If decision is SHORTLIST or HOLD

Generate 3-5 interview focus topics.

If decision is REJECT

Interview focus should be empty.

Also provide

Strengths

Weaknesses

Improvement Suggestions

Reasoning

Return only structured JSON.
"""


def screen_candidate(jd, candidate):

    evidence = "\n\n".join(candidate["evidence"])

    prompt = f"""
JOB DESCRIPTION

{jd.model_dump_json(indent=2)}

------------------------------------

Candidate Name

{candidate['candidate_name']}

------------------------------------

Resume Evidence

{evidence}
"""

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=[
            SYSTEM_PROMPT,
            prompt
        ],

        config={

            "response_schema": ScreeningSchema,

            "response_mime_type": "application/json"

        }

    )

    result = response.parsed

    mandatory = len(jd.mandatory_skills)

    matched = len(result.mandatory_skills_matched)

    percentage = 0

    if mandatory > 0:

        percentage = int((matched / mandatory) * 100)

    result.mandatory_match_percentage = percentage

    if percentage >= 80:

        result.decision = "SHORTLIST"

    elif percentage >= 50:

        result.decision = "HOLD"

    else:

        result.decision = "REJECT"

    return result

if __name__ == "__main__":

    from rag.loader import load_job_description
    from nodes.parse_jd import parse_job_description
    from rag.retriever import retrieve_candidate_evidence

    jd_text = load_job_description(
        "ai_engineer.txt"
    )

    jd = parse_job_description(jd_text)

    candidates = retrieve_candidate_evidence(
        jd.description
    )

    print("=" * 70)
    print("SCREENING RESULTS")
    print("=" * 70)

    for candidate in candidates:

        result = screen_candidate(jd, candidate)

        print("=" * 70)

        print("Candidate :", result.candidate_name)

        print()

        print("Mandatory Match :", result.mandatory_match_percentage, "%")

        print("Overall Score   :", result.overall_match_score)

        print("Decision        :", result.decision)

        print()

        print("Matched Mandatory Skills")

        print(result.mandatory_skills_matched)

        print()

        print("Missing Mandatory Skills")

        print(result.mandatory_skills_missing)

        print()

        print("Preferred Skills")

        print(result.preferred_skills_matched)

        print()

        print("Strengths")

        for s in result.strengths:
            print("✓", s)

        print()

        print("Weaknesses")

        for w in result.weaknesses:
            print("-", w)

        print()

        print("Improvement Suggestions")

        for s in result.improvement_suggestions:
            print("•", s)

        print()

        print("Interview Focus")

        for t in result.interview_focus:
            print("•", t)

        print()

        print("Reason")

        print(result.reasoning)

        print("=" * 70)