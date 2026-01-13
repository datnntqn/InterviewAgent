"""
Pydantic Output Models for CrewAI Tasks

These models define the structured output format for each task,
ensuring type safety and validation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict


class SkillClassification(BaseModel):
    """Classification of skills into must-have and nice-to-have."""
    must_have: List[str] = Field(description="Critical skills required for the job")
    nice_to_have: List[str] = Field(description="Bonus skills that are preferred")


class JobAnalysisOutput(BaseModel):
    """Output model for job description analysis task."""
    technical_skills: List[str] = Field(description="List of technical skills required")
    soft_skills: List[str] = Field(description="List of soft skills and behavioral requirements")
    experience_required: str = Field(description="Years of experience required (e.g., '5+ years')")
    skill_classification: SkillClassification = Field(description="Skills classified by priority")
    skill_gaps: List[str] = Field(description="Skills the candidate is missing")
    candidate_strengths: List[str] = Field(description="Skills where the candidate excels")
    recommendations: List[str] = Field(description="Actionable recommendations for interview prep")
    match_percentage: int = Field(description="Overall match score (0-100)", ge=0, le=100)


class CompanyCultureOutput(BaseModel):
    """Output model for company culture research task."""
    company_name: str = Field(description="Name of the company")
    mission_statement: str = Field(description="The company's mission statement")
    core_values: List[str] = Field(description="List of company's core values")
    work_culture: str = Field(description="Description of the work culture and environment")
    recent_initiatives: List[str] = Field(description="Recent projects, initiatives, or achievements")
    culture_fit_tips: List[str] = Field(description="Tips for demonstrating culture fit in interview")
    key_themes: List[str] = Field(description="Key cultural themes identified")


class TechnicalQuestion(BaseModel):
    """A technical interview question."""
    question: str = Field(description="The technical question")
    difficulty: str = Field(description="Difficulty level: easy, medium, or hard")
    skills_tested: List[str] = Field(description="Skills being tested by this question")


class STARFramework(BaseModel):
    """STAR method framework for behavioral questions."""
    situation: str = Field(description="What to describe about the context")
    task: str = Field(description="What was your responsibility")
    action: str = Field(description="What actions you took")
    result: str = Field(description="What was the outcome")


class BehavioralQuestion(BaseModel):
    """A behavioral interview question with STAR framework."""
    question: str = Field(description="The behavioral question")
    star_framework: STARFramework = Field(description="STAR method guidance")
    competency_tested: str = Field(description="The competency being evaluated")


class CompanySpecificQuestion(BaseModel):
    """A company-specific interview question."""
    question: str = Field(description="The company-specific question")
    related_value: str = Field(description="The company value this relates to")
    suggested_approach: str = Field(description="How to approach answering this question")


class InterviewStrategy(BaseModel):
    """Interview preparation strategy."""
    preparation_roadmap: List[str] = Field(description="Step-by-step preparation plan")
    key_talking_points: List[str] = Field(description="Important points to emphasize")
    addressing_gaps: List[str] = Field(description="How to address skill gaps")
    culture_fit_approach: List[str] = Field(description="Tips for demonstrating culture fit")


class InterviewDossierOutput(BaseModel):
    """Output model for interview dossier preparation task."""
    technical_questions: List[TechnicalQuestion] = Field(description="List of technical questions")
    behavioral_questions: List[BehavioralQuestion] = Field(description="List of behavioral questions with STAR framework")
    company_specific_questions: List[CompanySpecificQuestion] = Field(description="List of company-specific questions")
    interview_strategy: InterviewStrategy = Field(description="Comprehensive interview strategy")
    questions_to_ask_interviewer: List[str] = Field(description="Questions for the candidate to ask")
