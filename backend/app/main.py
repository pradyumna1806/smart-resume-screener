from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from pydantic_settings import BaseSettings
from app.database.match_repository import ensure_match_index

from app.api.resumes import router as resume_router
from app.api.jobs import router as jobs_router
from app.database.mongodb import(
    close_mongodb_connection,
    connect_to_mongodb,
)
from app.api.matches import router as matches_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    await ensure_match_index()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title = "Smart Resume Screener API",
    description = "AI-powered resume screening and candidate matching API",
    version = "1.0.0",
    lifespan = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(matches_router)

@app.get("/api/health")
async def health_check():
    return {
        "status" : "healthy",
        "service" : "smart-resume-screener",
    }

