"""
rewrite_jd.py

Improves the quality of a Job Description.
"""

from google import genai

from config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are an experienced HR recruiter.

Rewrite the given Job Description professionally.

Rules:
1. Do NOT add new skills.
2. Do NOT remove mandatory skills.
3. Keep the meaning unchanged.
4. Improve readability and formatting.
5. Make it attractive to candidates.
6. Preserve all technical requirements.
7. Return only the rewritten Job Description.
"""


def rewrite_job_description(jd):

    prompt = f"""
Rewrite the following Job Description.

Job Title:
{jd.job_title}

Location:
{jd.location}

Employment Type:
{jd.employment_type}

Experience:
{jd.experience}

Education:
{jd.education}

Mandatory Skills:
{", ".join(jd.mandatory_skills)}

Preferred Skills:
{", ".join(jd.preferred_skills)}

Responsibilities:
{chr(10).join(jd.responsibilities)}

Original Job Description:
{jd.description}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            SYSTEM_PROMPT,
            prompt
        ]
    )

    return response.text

def save_rewritten_jd(
    rewritten_jd: str,
    filename: str = "Rewritten_Job_Description.txt"
):
    """
    Save the rewritten job description to a text file.
    """

    with open(filename, "w", encoding="utf-8") as file:

        file.write("=" * 80 + "\n")
        file.write("HIREPILOT AI - REWRITTEN JOB DESCRIPTION\n")
        file.write("=" * 80 + "\n\n")

        file.write(rewritten_jd)

    print(f"✓ Rewritten JD saved to {filename}")

if __name__ == "__main__":

    from rag.loader import load_job_description
    from nodes.parse_jd import parse_job_description

    jd_text = load_job_description("ai_engineer.txt")

    jd = parse_job_description(jd_text)

    rewritten = rewrite_job_description(jd)

    print("\n" + "=" * 70)
    print("REWRITTEN JOB DESCRIPTION")
    print("=" * 70)
    print(rewritten)

    