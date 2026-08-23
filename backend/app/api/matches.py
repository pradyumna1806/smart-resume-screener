from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.database.candidate_repository import get_candidate
from app.database.job_repository import get_job
from app.schemas.match_api import MatchRequest
from app.schemas.candidate import CandidateProfile
from app.schemas.job import JobProfile
from app.services.matching_service import match_candidate_to_job
from app.database.match_repository import (
    create_match as save_match,
    get_match,
    get_match_by_candidate_and_job,
    get_all_matches,
)


router = APIRouter(
    prefix="/api/matches",
    tags=["Matches"],
)


@router.post("")
async def create_match(request: MatchRequest):

    try:
        candidate = await get_candidate(request.candidate_id)
        job = await get_job(request.job_id)

        if not candidate:
            raise HTTPException(
                status_code=404,
                detail="Candidate not found.",
            )

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found.",
            )

        candidate_profile = CandidateProfile.model_validate(candidate)

        job_data = {
            key: value
            for key, value in job.items()
            if key not in {
                "_id",
                "original_description",
                "created_at",
                "updated_at",
            }
        }

        job_profile = JobProfile.model_validate(job_data)

        existing_match = await get_match_by_candidate_and_job(
            candidate_id=request.candidate_id,
            job_id=request.job_id,
        )

        if existing_match:
            existing_match["_id"] = str(existing_match["_id"])
            existing_match["candidate_id"] = str(existing_match["candidate_id"])
            existing_match["job_id"] = str(existing_match["job_id"])

            return existing_match

        result = await match_candidate_to_job(
            candidate=candidate_profile,
            job=job_profile,
            original_job_description=job["original_description"],
        )

        match_id = await save_match(
            candidate_id=request.candidate_id,
            job_id=request.job_id,
            result=result,
        )

        return {
            "match_id": match_id,
            "candidate_id": request.candidate_id,
            "job_id": request.job_id,
            "match": result,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Match preparation failed: {exc}",
        ) from exc


@router.get("/{match_id}")
async def get_saved_match(match_id: str):

    try:
        match = await get_match(match_id)

        if not match:
            raise HTTPException(
                status_code=404,
                detail="Match not found.",
            )

        match["_id"] = str(match["_id"])
        match["candidate_id"] = str(match["candidate_id"])
        match["job_id"] = str(match["job_id"])

        return match

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve match: {exc}",
        ) from exc

@router.get("")
async def list_matches():

    try:
        matches = await get_all_matches()

        for match in matches:
            match["_id"] = str(match["_id"])
            match["candidate_id"] = str(match["candidate_id"])
            match["job_id"] = str(match["job_id"])

        return {
            "matches": matches,
            "count": len(matches),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve matches: {exc}",
        ) from exc