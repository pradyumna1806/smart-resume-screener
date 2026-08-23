from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.job import JobProfile


client = genai.Client(api_key=settings.gemini_api_key)


async def extract_job_profile(
    job_description: str,
) -> JobProfile:

    prompt = f"""
You are an expert job-description analysis system.

Your task is to convert the job description into structured matching
signals for a resume screening system.

IMPORTANT:
The job description may have ANY structure.

It may:
- contain a dedicated skills section,
- describe skills only inside responsibilities,
- mix technical requirements with business requirements,
- mention technologies indirectly through activities,
- contain repeated information,
- use abbreviations,
- use different terminology for the same concept.

Do NOT assume that headings such as "Skills", "Qualifications",
"Requirements", or "Responsibilities" exist.

Extract information from the ENTIRE job description.

RULES:

1. keywords
Extract concrete, matchable concepts such as:
- programming languages
- frameworks
- libraries
- platforms
- databases
- cloud technologies
- AI/ML technologies
- tools
- methodologies
- technical concepts
- business/domain concepts when they are important to the role.

If an abbreviation or alternate name clearly refers to a known concept,
use the commonly recognized concept name.

For example:
- JS → JavaScript
- sklearn → scikit-learn
- K8s → Kubernetes
- AWS → Amazon Web Services

These are examples, NOT a fixed alias list.
Apply the same reasoning to other obvious abbreviations and
alternate terminology.

If the meaning is genuinely ambiguous, preserve the wording rather
than inventing an interpretation.

2. domain_terms
Extract important industry, business, or subject-matter concepts.

3. responsibilities
Extract meaningful activities the candidate is expected to perform.
Do not simply copy entire paragraphs.

4. experience_signals
Extract explicit signals about experience, seniority, analytical
ability, project experience, leadership, deadlines, collaboration,
or similar expectations.

5. education_signals
Extract explicit education, degree, academic, or field-of-study
requirements or preferences.

6. Do not invent requirements.
Only extract information supported by the job description.

7. Do not assign importance, mandatory/optional status, or scores.
The matching engine will make those judgments later.

8. Avoid meaningless generic words such as:
"team", "work", "good", "excellent", "company", unless they carry
specific matching meaning.

9. Preserve important technical names accurately.

Return only the structured information requested by the schema.

JOB DESCRIPTION:
-----------------
{job_description}
-----------------
"""

    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=JobProfile.model_json_schema(),
        ),
    )

    return JobProfile.model_validate_json(response.text)