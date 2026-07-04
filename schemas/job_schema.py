"""
job_schema.py

Pydantic schema representing a structured Job Description.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class JobSchema(BaseModel):

    # ---------------------------------------------------
    # Basic Information
    # ---------------------------------------------------

    job_title: str = Field(
        description="Job title"
    )

    company_name: Optional[str] = Field(
        default=None,
        description="Company name if available"
    )

    location: Optional[str] = Field(
        default=None,
        description="Job location"
    )

    employment_type: Optional[str] = Field(
        default=None,
        description="Full-time, Internship, Contract etc."
    )

    experience: Optional[str] = Field(
        default=None,
        description="Required experience"
    )

    education: Optional[str] = Field(
        default=None,
        description="Minimum education qualification"
    )

    # ---------------------------------------------------
    # Skills
    # ---------------------------------------------------

    mandatory_skills: List[str] = Field(
        default_factory=list,
        description="Must-have technical skills"
    )

    preferred_skills: List[str] = Field(
        default_factory=list,
        description="Nice-to-have skills"
    )

    # ---------------------------------------------------
    # Responsibilities
    # ---------------------------------------------------

    responsibilities: List[str] = Field(
        default_factory=list,
        description="Main job responsibilities"
    )

    # ---------------------------------------------------
    # Keywords
    # ---------------------------------------------------

    keywords: List[str] = Field(
        default_factory=list,
        description="Important keywords extracted from JD"
    )

    # ---------------------------------------------------
    # Original Description
    # ---------------------------------------------------

    description: str = Field(
        description="Original Job Description"
    )