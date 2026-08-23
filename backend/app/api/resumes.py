from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.candidate import CandidateProfile
from app.services.llm_service import extract_candidate_profile
from app.services.resume_parser import extract_text_from_pdf
from app.database.candidate_repository import create_candidate


router = APIRouter(
    prefix = "/api/resumes",
    tags = ["Resumes"],
)

@router.post("/extract")
async def extract_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code = 400,
            detail = "Only PDF files are supported.",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code = 400,
            detail = "Uploaded file is empty.",
        )

    try:
        resume_text = extract_text_from_pdf(file_bytes)

        if not resume_text:
            raise HTTPException(
                status_code = 400,
                detail = "Could not extract text from the PDF.",
            )

        candidate = await extract_candidate_profile(resume_text)

        candidate_id = await create_candidate(
            profile = candidate,
            filename = file.filename or "unknown.pdf",
        )

        return {
            "candidate_id" : candidate_id,
            "candidate" : candidate,
        }

    except HTTPException:
        raise
        
    except Exception as exc:
        raise HTTPException(
            status_code = 500,
            detail = f"Resume processing failed : {exc}",
        ) from exc
