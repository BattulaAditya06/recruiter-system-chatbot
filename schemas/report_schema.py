from typing import List
from pydantic import BaseModel


class CandidateReport(BaseModel):

    candidate_name: str

    decision: str

    overall_score: int

    mandatory_match: int

    matched: List[str]

    missing: List[str]

    preferred: List[str]

    strengths: List[str]

    weaknesses: List[str]

    improvements: List[str]

    interview_focus: List[str]

    reasoning: str


class FinalReport(BaseModel):

    job_title: str

    candidates_screened: int

    shortlisted: int

    hold: int

    rejected: int

    reports: List[CandidateReport]