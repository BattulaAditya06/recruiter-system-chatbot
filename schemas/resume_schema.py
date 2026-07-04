from pydantic import BaseModel, Field


class ResumeSchema(BaseModel):
    """
    Structured representation of a candidate resume.
    """

    candidate_name: str = Field(
        description="Candidate full name."
    )

    email: str = Field(
        default="Not Available",
        description="Candidate email."
    )

    phone: str = Field(
        default="Not Available",
        description="Candidate phone number."
    )

    experience: str = Field(
        default="Not Mentioned",
        description="Total experience."
    )

    education: str = Field(
        default="Not Mentioned",
        description="Highest qualification."
    )

    technical_skills: list[str] = Field(
        default_factory=list,
        description="Technical skills."
    )

    projects: list[str] = Field(
        default_factory=list,
        description="Major projects."
    )

    certifications: list[str] = Field(
        default_factory=list,
        description="Certifications."
    )

    summary: str = Field(
        default="",
        description="Professional summary."
    )