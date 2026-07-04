"""
screening_schema.py
"""

from typing import List
from pydantic import BaseModel, Field


class ScreeningSchema(BaseModel):

    candidate_name: str

    mandatory_match_percentage: int = Field(
        description="Percentage of mandatory skills matched"
    )

    overall_match_score: int = Field(
        description="Overall score between 0 and 100"
    )

    decision: str = Field(
        description="SHORTLIST, HOLD or REJECT"
    )

    mandatory_skills_matched: List[str] = Field(default_factory=list)

    mandatory_skills_missing: List[str] = Field(default_factory=list)

    preferred_skills_matched: List[str] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    weaknesses: List[str] = Field(default_factory=list)

    improvement_suggestions: List[str] = Field(default_factory=list)

    interview_focus: List[str] = Field(default_factory=list)

    reasoning: str