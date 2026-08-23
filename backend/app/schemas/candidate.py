from pydantic import BaseModel, Field

class Education(BaseModel):
    degree : str | None = None
    institution : str | None = None
    graduation_year : int | None = None

class Experience(BaseModel):
    company : str | None = None
    role : str | None = None
    duration : str | None = None
    responsibilities : list[str] = Field(default_factory = list)

class Project(BaseModel):
    name : str | None = None
    description : str | None = None
    technologies : list[str] = Field(default_factory = list)

class Certification(BaseModel):
    name : str | None = None
    issuer : str | None = None
    year : int | None = None

class CandidateProfile(BaseModel):
    name : str | None = None
    email : str | None = None
    phone : str | None = None
    location : str | None = None

    skills : list[str] = Field(default_factory = list)
    education : list[Education] = Field(default_factory = list)
    experience : list[Experience] = Field(default_factory = list)
    projects : list[Project] = Field(default_factory = list)
    certificaitons : list[Certification] = Field(default_factory = list)
    

