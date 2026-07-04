"""
graph/state.py

Shared state passed between LangGraph nodes.
"""

from typing import TypedDict, List, Optional

from schemas.job_schema import JobSchema
from schemas.report_schema import FinalReport
from schemas.screening_schema import ScreeningResult
from schemas.interview_schema import InterviewSchema


class GraphState(TypedDict):

    # Raw Input
    job_description: str

    # Parsed JD
    parsed_job: Optional[JobSchema]

    # Rewritten JD
    rewritten_job: Optional[str]

    # Retrieved Candidates
    retrieved_candidates: List[dict]

    # Screening Results
    screened_candidates: List[ScreeningResult]

    # Interview Questions
    interview_questions: List[InterviewSchema]

    # Recruiter Decision
    approval: bool

    # Final Report
    final_report: Optional[FinalReport]