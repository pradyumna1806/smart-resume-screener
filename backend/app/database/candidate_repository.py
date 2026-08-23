from datetime import datetime, timezone
from bson import ObjectId
from app.database.mongodb import mongodb
from app.schemas.candidate import CandidateProfile

COLLECTION_NAME = "candidates"

async def create_candidate(
        profile : CandidateProfile,
        filename : str,
) -> str:
    document = {
        **profile.model_dump(),
        "source_filename" : filename,
        "created_at" : datetime.now(timezone.utc),
        "updated_at" : datetime.now(timezone.utc),
    }

    result = await mongodb.database[COLLECTION_NAME].insert_one(document)

    return str(result.inserted_id)

async def get_candidate(candidate_id: str):
    document = await mongodb.database[COLLECTION_NAME].find_one(
        {"_id": ObjectId(candidate_id)}
    )

    return document
