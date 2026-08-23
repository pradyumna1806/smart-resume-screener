from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.candidate import CandidateProfile

client = genai.Client(api_key = settings.gemini_api_key)

async def extract_candidate_profile(
    resume_text : str,
) -> CandidateProfile:

    prompt = f"""
You are an expert resume information extraction system.

Extract factual information from the resume below.

Rules:
- Extract only information explicitly present in the resume.
- Do not invent or infer missing information.
- If a field is not present, return null or an empty list.
- Preserve the candidate's actual skills.
- Separate education and work experience accurately.
- Extract projects separately even if they are academic or personal projects.
- Extract certifications separately.
- Preserve education accurately.
- A leadership role may be included as experience if it represents a significant role or responsibility.
- Keep responsibilities concise but factual.
- Keep project descriptions concise but factual.
- Return only the requested structured information.

Resume : 
-----------------
{resume_text}
-----------------
"""

    response = await client.aio.models.generate_content(
        model = settings.gemini_model,
        contents = prompt,
        config = types.GenerateContentConfig(
            response_mime_type = "application/json",
            response_json_schema = CandidateProfile.model_json_schema(),
        ),
    )

    return CandidateProfile.model_validate_json(response.text)

