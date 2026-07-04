from pydantic import BaseModel, Field


class CandidateSchema(BaseModel):
    """
    Final evaluation of a candidate after resume screening.

    This object is generated after:
    Resume Parsing
            ↓
    RAG Retrieval
            ↓
    LLM Analysis

    It is the primary object shown to the recruiter.
    """

    # --------------------------
    # Candidate Information
    # --------------------------

    candidate_name: str = Field(
        description="Candidate full name."
    )

    email: str = Field(
        default="Not Available",
        description="Candidate email."
    )

    experience: str = Field(
        default="Not Mentioned",
        description="Years of professional experience."
    )

    # --------------------------
    # Matching
    # --------------------------

    match_score: float = Field(
        ge=0,
        le=100,
        description="Overall JD matching score."
    )

    confidence: str = Field(
        description="High / Medium / Low confidence."
    )

    # --------------------------
    # Skill Analysis
    # --------------------------

    matched_skills: list[str] = Field(
        default_factory=list,
        description="Skills matching the JD."
    )

    missing_skills: list[str] = Field(
        default_factory=list,
        description="Important missing skills."
    )

    transferable_skills: list[str] = Field(
        default_factory=list,
        description="Related skills that partially satisfy the JD."
    )

    # --------------------------
    # Recruiter Insights
    # --------------------------

    strengths: list[str] = Field(
        default_factory=list,
        description="Major strengths."
    )

    concerns: list[str] = Field(
        default_factory=list,
        description="Potential hiring concerns."
    )

    interview_focus: list[str] = Field(
        default_factory=list,
        description="Topics interviewer should focus on."
    )

    # --------------------------
    # Recommendation
    # --------------------------

    hiring_recommendation: str = Field(
        description="Proceed / Review / Reject"
    )

    recommendation_reason: str = Field(
        description="Short explanation."
    )

    # --------------------------
    # Explainability
    # --------------------------

    evidence: list[str] = Field(
        default_factory=list,
        description="Resume evidence supporting the recommendation."
    )