"""
graph/state.py

Shared workflow state used by LangGraph.
"""

from typing import TypedDict, List, Optional

from schemas.job_schema import JobSchema
from schemas.report_schema import FinalReport


class GraphState(TypedDict):

    # Raw Input
    job_description: str

    # Parsed Job Description
    parsed_job: Optional[JobSchema]

    # Rewritten JD
    rewritten_job: Optional[str]

    # Retrieved Candidates
    retrieved_candidates: List[dict]

    # Screening Results
    screened_candidates: List[dict]

    # Interview Questions
    interview_questions: List[dict]

    # Final Report
    final_report: Optional[FinalReport]

    reviewed_candidates: list