from pydantic import BaseModel, Field


class JobProfile(BaseModel):
    title: str | None = None
    keywords: list[str] = Field(default_factory=list)
    domain_terms: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    experience_signals: list[str] = Field(default_factory=list)
    education_signals: list[str] = Field(default_factory=list)