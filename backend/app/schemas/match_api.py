from pydantic import BaseModel


class MatchRequest(BaseModel):
    candidate_id: str
    job_id: str