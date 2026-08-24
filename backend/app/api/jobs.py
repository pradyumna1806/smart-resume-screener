from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.job_repository import (
    create_job,
    get_jobs,
)
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


@router.get("")
async def list_jobs(
    search: str = "",
    limit: int = 20,
):
    if limit < 1 or limit > 50:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 50.",
        )

    try:
        jobs = await get_jobs(
            search=search,
            limit=limit,
        )

        return {
            "jobs": jobs,
            "count": len(jobs),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve jobs: {exc}",
        ) from exc