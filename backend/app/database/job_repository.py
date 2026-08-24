from datetime import datetime, timezone
from bson import ObjectId
from app.database.mongodb import mongodb
from app.schemas.job import JobProfile


COLLECTION_NAME = "jobs"


async def create_job(
    profile: JobProfile,
    original_description: str,
) -> str:

    now = datetime.now(timezone.utc)

    document = {
        **profile.model_dump(),
        "original_description": original_description,
        "created_at": now,
        "updated_at": now,
    }

    result = await mongodb.database[COLLECTION_NAME].insert_one(
        document
    )

    return str(result.inserted_id)

async def get_job(job_id: str):
    document = await mongodb.database[COLLECTION_NAME].find_one(
        {"_id": ObjectId(job_id)}
    )

    return document


async def get_jobs(
    search: str = "",
    limit: int = 20,
):
    query = {}

    if search.strip():
        query = {
            "$or": [
                {"title": {"$regex": search.strip(), "$options": "i"}},
                {"keywords": {"$regex": search.strip(), "$options": "i"}},
                {"domain_terms": {"$regex": search.strip(), "$options": "i"}},
            ]
        }

    cursor = (
        mongodb.database[COLLECTION_NAME]
        .find(query)
        .sort("created_at", -1)
        .limit(limit)
    )

    jobs = await cursor.to_list(length=limit)

    for job in jobs:
        job["_id"] = str(job["_id"])

    return jobs