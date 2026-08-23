from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

from app.core.config import settings

class MongoDB:
    client: AsyncMongoClient | None = None
    database = None

mongodb = MongoDB()

async def connect_to_mongodb():
    mongodb.client = AsyncMongoClient(
        settings.mongodb_url,
        server_api = ServerApi(
            version = "1",
            strict = True,
            deprecation_errors = True,
        ),
        tlsDisableOCSPEndpointCheck = True,
    )

    await mongodb.client.admin.command("ping")

    mongodb.database = mongodb.client[settings.database_name]

    print("Connected to MongoDB")

async def close_mongodb_connection():
    if mongodb.client:
        await mongodb.client.close()
        print("MongoDB connection closed")

