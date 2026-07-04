from pydantic import BaseModel, Field

from schemas.candidate_schema import CandidateSchema


class ReportSchema(BaseModel):

    role: str

    total_applicants: int

    shortlisted_candidates: list[CandidateSchema]

    rewritten_jd: str

    salary_benchmark: str

    recruiter_decision: str