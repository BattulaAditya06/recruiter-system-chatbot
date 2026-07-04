"""
interview_schema.py
"""

from typing import List
from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    category: str
    question: str


class InterviewSchema(BaseModel):

    technical_questions: List[InterviewQuestion]

    project_questions: List[InterviewQuestion]

    behavioral_questions: List[InterviewQuestion]