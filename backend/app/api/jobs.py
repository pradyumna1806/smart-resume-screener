from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.job_repository import create_job
from app.services.job_service import extract_job_profile


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)


class JobDescriptionRequest(BaseModel):
    description: str


@router.post("/extract")
async def extract_job(request: JobDescriptionRequest):

    if not request.description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    try:
        job_profile = await extract_job_profile(
            request.description
        )

        job_id = await create_job(
            profile=job_profile,
            original_description=request.description,
        )

        return {
            "job_id": job_id,
            "job": job_profile,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Job processing failed: {exc}",
        ) from exc