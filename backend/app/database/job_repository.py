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