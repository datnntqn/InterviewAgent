from typing import List
from pydantic import BaseModel, Field


class JobDescriptionAnalysis(BaseModel):
    skills: List[str] = Field(..., description="Key technical and soft skills")
    keywords: List[str] = Field(..., description="Important keywords from JD")
    experience_years: int = Field(..., description="Required years of experience")


class CompanyCultureProfile(BaseModel):
    values: List[str] = Field(..., description="Company core values")
    mission: str = Field(..., description="Company mission statement")


class InterviewDossier(BaseModel):
    questions: List[str] = Field(..., description="Interview questions")
    strategy: str = Field(..., description="Interview strategy and focus areas")
