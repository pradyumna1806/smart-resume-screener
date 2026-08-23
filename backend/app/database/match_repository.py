from datetime import datetime, timezone

from bson import ObjectId

from app.database.mongodb import mongodb
from app.schemas.match import MatchResult


COLLECTION_NAME = "matches"


async def create_match(
    candidate_id: str,
    job_id: str,
    result: MatchResult,
) -> str:

    now = datetime.now(timezone.utc)

    document = {
        "candidate_id": ObjectId(candidate_id),
        "job_id": ObjectId(job_id),
        "result": result.model_dump(),
        "created_at": now,
        "updated_at": now,
    }

    response = await mongodb.database[COLLECTION_NAME].insert_one(
        document
    )

    return str(response.inserted_id)


async def get_match(match_id: str):
    document = await mongodb.database[COLLECTION_NAME].find_one(
        {"_id": ObjectId(match_id)}
    )

    return document


async def get_match_by_candidate_and_job(
    candidate_id: str,
    job_id: str,
):
    document = await mongodb.database[COLLECTION_NAME].find_one(
        {
            "candidate_id": ObjectId(candidate_id),
            "job_id": ObjectId(job_id),
        }
    )

    return document

async def ensure_match_index():
    await mongodb.database[COLLECTION_NAME].create_index(
        [
            ("candidate_id", 1),
            ("job_id", 1),
        ],
        unique=True,
    )

async def get_all_matches():
    cursor = mongodb.database[COLLECTION_NAME].find(
        {}
    ).sort("created_at", -1)

    return await cursor.to_list(length=None)