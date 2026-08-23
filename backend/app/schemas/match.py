from pydantic import BaseModel, Field


class RequirementMatch(BaseModel):
    job_requirement: str
    candidate_evidence: str
    match_type: str
    explanation: str

class EligibilityRequirement(BaseModel):
    requirement: str
    candidate_evidence: str
    status: str
    explanation: str

class SkillGap(BaseModel):
    job_requirement: str
    explanation: str


class MatchScores(BaseModel):
    technical_fit: int = Field(ge=0, le=40)
    responsibility_fit: int = Field(ge=0, le=25)
    domain_fit: int = Field(ge=0, le=15)
    experience_fit: int = Field(ge=0, le=10)
    education_fit: int = Field(ge=0, le=10)


class MatchResult(BaseModel):
    overall_score: int = Field(ge=0, le=100)

    recommendation: str

    scores: MatchScores

    matched_requirements: list[RequirementMatch] = Field(
        default_factory=list
    )

    eligibility_requirements: list[EligibilityRequirement] = Field(
        default_factory=list
    )

    skill_gaps: list[SkillGap] = Field(
        default_factory=list
    )

    strengths: list[str] = Field(
        default_factory=list
    )

    gaps: list[str] = Field(
        default_factory=list
    )

    justification: str