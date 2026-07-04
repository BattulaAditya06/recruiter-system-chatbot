"""
screen_candidates.py

Evaluates retrieved candidates against the Job Description.
"""

from google import genai

from config import GEMINI_API_KEY
from config import MODEL_NAME
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

DSA = Data Structures and Algorithms

OOP = Object Oriented Programming

ML = Machine Learning

4. Match mandatory skills.

5. Match preferred skills.

6. Identify strengths.

7. Identify weaknesses.

8. Suggest improvements.

9. Generate interview focus topics.

IMPORTANT

Do NOT assign scores.

Do NOT decide SHORTLIST/HOLD/REJECT.

The application will calculate them.

Return only structured JSON.
"""


def screen_candidate(jd, candidate):

    evidence = "\n\n".join(candidate["evidence"])

    prompt = f"""
JOB DESCRIPTION

{jd.model_dump_json(indent=2)}

Candidate

{candidate["candidate_name"]}

Resume

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

    mandatory_total = len(jd.mandatory_skills)

    matched = len(result.mandatory_skills_matched)

    mandatory_percentage = int(
        matched / mandatory_total * 100
    ) if mandatory_total else 0

    preferred_total = len(jd.preferred_skills)

    preferred = len(result.preferred_skills_matched)

    preferred_percentage = int(
        preferred / preferred_total * 100
    ) if preferred_total else 0

    overall_score = mandatory_percentage

    if preferred_percentage >= 50:
        overall_score += 5

    overall_score = min(overall_score, 100)

    if mandatory_percentage >= 80:

        decision = "SHORTLIST"

    elif mandatory_percentage >= 50:

        decision = "HOLD"

    else:

        decision = "REJECT"

    return {

        "candidate_name": result.candidate_name,

        "mandatory_match": mandatory_percentage,

        "overall_score": overall_score,

        "decision": decision,

        "matched": result.mandatory_skills_matched,

        "missing": result.mandatory_skills_missing,

        "preferred": result.preferred_skills_matched,

        "strengths": result.strengths,

        "weaknesses": result.weaknesses,

        "improvements": result.improvement_suggestions,

        "interview_focus": result.interview_focus,

        "reasoning": result.reasoning

    }

if __name__ == "__main__":

    from rag.loader import load_job_description
    from nodes.parse_jd import parse_job_description
    from rag.retriever import retrieve_candidate_evidence

    jd_text = load_job_description("ai_engineer.txt")

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

        print("Candidate :", result["candidate_name"])
        print()

        print("Mandatory Match :", result["mandatory_match"], "%")
        print("Overall Score   :", result["overall_score"])
        print("Decision        :", result["decision"])
        print()

        print("Matched Mandatory Skills")
        for skill in result["matched"]:
            print(f"  ✓ {skill}")

        print()

        print("Missing Mandatory Skills")
        for skill in result["missing"]:
            print(f"  ✗ {skill}")

        print()

        print("Preferred Skills")
        if result["preferred"]:
            for skill in result["preferred"]:
                print(f"  • {skill}")
        else:
            print("  None")

        print()

        print("Strengths")
        for strength in result["strengths"]:
            print(f"  ✓ {strength}")

        print()

        print("Weaknesses")
        for weakness in result["weaknesses"]:
            print(f"  ✗ {weakness}")

        print()

        print("Improvement Suggestions")
        for suggestion in result["improvements"]:
            print(f"  • {suggestion}")

        print()

        print("Interview Focus")
        if result["interview_focus"]:
            for topic in result["interview_focus"]:
                print(f"  • {topic}")
        else:
            print("  None")

        print()

        print("Reasoning")
        print(result["reasoning"])

        print("=" * 70)
        print()