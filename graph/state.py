from typing_extensions import TypedDict


class RecruitmentState(TypedDict):

    user_query: str

    intent: str

    jd_text: str

    parsed_jd: dict

    resumes: list

    resume_count: int

    shortlisted_candidates: list

    selected_candidate: dict

    rewritten_jd: str

    interview_questions: list

    salary_benchmark: str

    recruiter_decision: str

    final_report: str