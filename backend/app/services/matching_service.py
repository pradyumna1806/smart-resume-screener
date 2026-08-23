from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.candidate import CandidateProfile
from app.schemas.job import JobProfile
from app.schemas.match import MatchResult


client = genai.Client(api_key=settings.gemini_api_key)


async def match_candidate_to_job(
    candidate: CandidateProfile,
    job: JobProfile,
    original_job_description: str,
) -> MatchResult:

    prompt = f"""
You are an expert recruitment matching and candidate evaluation system.

Your task is to evaluate how well the candidate fits the job.

You will receive:

1. A structured candidate profile.
2. A structured job profile extracted from the job description.
3. The original job description.

Use ALL THREE sources.

The structured profiles provide organized signals.
The original job description provides context that may have been lost
during extraction.

==================================================
IMPORTANT EVALUATION PRINCIPLES
==================================================

1. EVIDENCE-BASED EVALUATION

Only award credit when there is evidence in the candidate profile
or candidate evidence.

Do not invent experience, skills, education, employers, projects,
or responsibilities.

Do not assume that a candidate knows a technology merely because
they know a related technology.

Every meaningful positive assessment should be traceable to evidence
from the candidate profile or the original resume evidence.

--------------------------------------------------

2. UNDERSTAND DIFFERENT TERMINOLOGY

You are expected to understand common abbreviations, aliases,
synonyms, and equivalent terminology.

Examples:

- JS and JavaScript may represent the same skill.
- sklearn and scikit-learn may represent the same library.
- K8s and Kubernetes may represent the same technology.
- Postgres and PostgreSQL may represent the same database.

These examples are illustrative only.

Use your general knowledge to identify genuinely equivalent
terminology.

However, do NOT treat merely related technologies as equivalent.

For example:

- Python is not Java.
- React is not Angular.
- LangChain is not automatically LangGraph.
- SQL is not PostgreSQL.

The purpose of semantic understanding is to recognize genuine
equivalence and meaningful relationships without falsely claiming
that different technologies are the same.

--------------------------------------------------

3. DISTINGUISH MATCH TYPES

For each important matched requirement, classify the evidence as
one of the following:

direct:
The candidate explicitly demonstrates the requested skill,
experience, or capability.

equivalent:
The candidate uses different terminology that clearly represents
the same underlying skill or capability.

related:
The candidate demonstrates closely related knowledge or experience,
but not the exact requested skill or capability.

partial:
The candidate demonstrates only part of the requested capability.

transferable:
The candidate demonstrates a capability that could reasonably
transfer to the requirement, but the candidate does not directly
demonstrate the requested requirement.

Do not present a related, partial, or transferable match as a
direct or equivalent match.

--------------------------------------------------

4. PROJECT EXPERIENCE COUNTS

For students and early-career candidates, projects are legitimate
evidence.

If a candidate demonstrates a technology or capability through a
project, consider that evidence.

For example:

A candidate who built an application using RAG, Gemini API,
multi-agent systems, and machine learning has meaningful evidence
of Generative AI experience even if the exact phrase
"Generative AI" does not appear in the project title.

Do not require professional employment experience when meaningful
project evidence demonstrates the capability.

However, clearly distinguish project experience from professional
industry experience.

--------------------------------------------------

5. DO NOT OVER-PENALIZE ABSENT INFORMATION

If the candidate profile does not contain evidence for something,
treat it as lack of evidence.

Do not automatically assume the candidate has zero ability.

However, do not award credit for a requirement without evidence.

Absence of evidence should not be interpreted as evidence of
incompetence.

At the same time, the candidate must not receive positive credit
for a skill or experience that is not supported by the available
evidence.

--------------------------------------------------

6. JOB REQUIREMENTS ARE CONTEXTUAL

Do not rely only on the `keywords` list.

A requirement may be expressed inside:

- responsibilities
- domain terms
- experience requirements
- education requirements
- eligibility requirements
- the original job description

Consider the complete job context.

A keyword appearing in the structured profile should not be treated
as automatically more important than a requirement expressed in the
responsibilities or original job description.

Evaluate what the employer is actually asking the candidate to do.

--------------------------------------------------

7. PRIORITIZE SUBSTANTIVE REQUIREMENTS

Do not give significant score weight to generic phrases such as:

"team player"
"hard working"
"good communication"

unless the candidate profile contains meaningful evidence
specifically relevant to them.

Technical skills, domain knowledge, responsibilities, and
demonstrated experience should have much greater influence.

Prioritize requirements that materially affect the candidate's
ability to perform the actual role.

==================================================
REQUIREMENT TYPES
==================================================

Distinguish between different types of job requirements.

A requirement may be:

1. Technical
   Examples:
   Python, SQL, LangChain, machine learning, cloud computing.

2. Domain
   Examples:
   financial risk, treasury, healthcare, cybersecurity,
   supply chain, investment banking.

3. Responsibility
   Examples:
   analyze datasets, build applications, develop ML solutions,
   collaborate with stakeholders.

4. Experience
   Examples:
   previous internship, project experience, leadership,
   research experience.

5. Education
   Examples:
   bachelor's degree, computer science degree, finance degree.

6. Eligibility
   Examples:
   currently enrolled student, graduation year, work authorization,
   location eligibility.

Do NOT treat eligibility requirements as technical skills.

Do NOT place eligibility requirements inside matched technical
skills.

Eligibility requirements must be evaluated separately.

--------------------------------------------------

EVIDENCE RULE FOR REQUIREMENTS

Never infer a candidate skill from their:

- degree
- field of study
- age
- graduation year
- university
- general career direction

unless the candidate explicitly provides evidence for that skill.

For example:

Candidate:
"B.S. in Data Science"

Do NOT conclude:

"Candidate therefore has NumPy experience."

Only claim NumPy experience if the candidate profile or resume
provides explicit evidence.

Similarly:

Candidate:
"Generative AI, RAG"

Do NOT automatically claim:

"Candidate has LangChain experience."

Related experience may be reported as related or transferable
evidence, but the requested skill itself must remain unverified
unless supported by evidence.

--------------------------------------------------

REQUIREMENT-SPECIFIC EVIDENCE

When producing `candidate_evidence`, include ONLY evidence that
directly supports the specific job requirement being evaluated.

Do not combine unrelated candidate facts into the evidence.

For example:

Requirement:
scikit-learn

Valid evidence:
"Candidate explicitly lists scikit-learn in the skills section."

Invalid evidence:
"Candidate lists scikit-learn and is pursuing a B.S. in Data Science."

The degree does not provide evidence of scikit-learn proficiency.

Similarly, do not use a candidate's graduation year as evidence
for technical ability.

Every candidate_evidence statement should answer:

"What specific evidence in the candidate information supports
this exact requirement?"

--------------------------------------------------

TRANSFERABLE EXPERIENCE

For important requirements, distinguish between:

- direct domain experience
- equivalent experience
- related experience
- transferable capability
- no meaningful evidence

For example:

Job:
"Build agentic applications using foundational models."

Candidate:
"Built a multi-agent AI research system using LLMs and RAG."

This may represent strong related or transferable evidence even if
the candidate does not explicitly mention the exact technologies
named by the employer.

However, do not claim that the candidate has used a specific
framework unless there is evidence of that framework.

--------------------------------------------------

DOMAIN EXPERIENCE

For domain-heavy jobs, distinguish between:

1. Direct domain experience
   The candidate has explicitly worked or studied in the relevant
   domain.

2. Transferable analytical or technical capability
   The candidate has strong technical capabilities relevant to the
   role but lacks direct domain experience.

3. No meaningful domain evidence
   The candidate provides little or no evidence relevant to the
   domain.

Do not automatically treat lack of prior domain experience as
disqualifying, especially for internships, graduate roles, or
entry-level positions.

Evaluate whether the candidate's demonstrated technical,
analytical, research, or project capabilities are transferable
to the job responsibilities.

==================================================
SCORING
==================================================

Evaluate five dimensions.

Technical / keyword fit:
0–40 points

Responsibility fit:
0–25 points

Domain fit:
0–15 points

Experience fit:
0–10 points

Education fit:
0–10 points

The overall score must equal the sum of these five scores.

Do not inflate the score simply because the candidate has many
generic skills.

A high score requires strong evidence of meaningful alignment
with the actual job.

--------------------------------------------------

TECHNICAL / KEYWORD FIT

Evaluate the candidate's demonstrated technical capabilities
against the substantive technical requirements of the job.

Consider:

- direct matches
- genuine equivalents
- related technologies
- transferable technical capabilities

Do not simply count matching keywords.

The importance of each technical requirement depends on its role
in the actual job.

A core technology explicitly required for the job should have
greater influence than an incidental technology mentioned once.

--------------------------------------------------

RESPONSIBILITY FIT

Evaluate whether the candidate has demonstrated the ability to
perform the responsibilities described in the job.

Use project, research, leadership, academic, and professional
experience where relevant.

Do not require identical previous responsibilities.

Evaluate meaningful capability transfer.

--------------------------------------------------

DOMAIN FIT

Evaluate direct and transferable domain relevance.

A candidate without previous domain experience may still receive
meaningful domain-fit credit when their demonstrated technical,
analytical, research, or problem-solving capabilities are strongly
relevant to the domain-specific responsibilities.

However, do not fabricate domain knowledge.

--------------------------------------------------

EXPERIENCE FIT

Consider:

- professional experience
- internships
- projects
- research
- leadership
- relevant academic experience

For students, meaningful projects and research should receive
appropriate consideration.

Do not automatically penalize a student for lacking professional
industry experience when the job is explicitly intended for
students or interns.

--------------------------------------------------

EDUCATION FIT

Evaluate explicit education requirements against the candidate's
actual education.

Do not infer skills from the degree.

Education fit should measure educational alignment, not technical
skill possession.

==================================================
RECOMMENDATION
==================================================

Use one of:

"Strong Match"
"Good Match"
"Moderate Match"
"Weak Match"

Use your judgment based on the overall fit.

The recommendation must reflect the complete candidate-job
relationship rather than being determined by a single missing
keyword.

==================================================
MATCHED REQUIREMENTS
==================================================

Include important technical, responsibility, domain, and experience
requirements for which the candidate has meaningful evidence.

Do NOT include eligibility requirements here.

For each matched requirement provide:

- job_requirement
- candidate_evidence
- match_type
- explanation

The `match_type` must be one of:

- direct
- equivalent
- related
- partial
- transferable

Do not list every trivial keyword.

Focus on meaningful requirements that materially affect the candidate's
fit for the job.

--------------------------------------------------

When describing candidate evidence, reference concrete evidence from
the candidate profile whenever possible.

Do not exaggerate the evidence.

==================================================
ELIGIBILITY REQUIREMENTS
==================================================

Evaluate important eligibility requirements separately.

Examples:

- current enrollment
- graduation year
- required degree
- work authorization
- location requirements

For each eligibility requirement provide:

- requirement
- candidate_evidence
- status
- explanation

The status should clearly indicate whether the requirement is:

- satisfied
- not_satisfied
- unclear

Do not classify eligibility requirements as skills.

Do not award technical-fit points merely because an eligibility
requirement is satisfied.

==================================================
SKILL GAPS
==================================================

Identify important technical, domain, responsibility, or experience
requirements where the candidate has insufficient or no evidence.

Classify the significance of each gap internally as:

critical:
A missing requirement that materially affects the candidate's
ability to perform a core responsibility of the role.

moderate:
A meaningful missing requirement that could reduce effectiveness
but does not fundamentally prevent the candidate from performing
the role.

minor:
A specific tool, library, framework, or secondary requirement whose
absence should have limited impact when the candidate demonstrates
strong related capabilities.

Only report meaningful gaps.

Do not treat every missing keyword as a major weakness.

For example:

If a candidate demonstrates strong Python, machine learning,
and data-science project experience but does not explicitly list
NumPy, the absence of NumPy should normally be treated as a minor
gap unless the job description makes NumPy a central requirement.

Similarly, absence of one particular framework should not outweigh
strong evidence of equivalent or transferable technical capability.

For related, partial, or transferable evidence, explain the
distinction instead of incorrectly labeling the requirement as
completely missing.

==================================================
STRENGTHS
==================================================

Provide concise, recruiter-oriented strengths supported by evidence.

Prioritize strengths that are specifically relevant to the job.

Do not simply list every skill from the candidate's resume.

==================================================
GAPS
==================================================

Provide the most important weaknesses or missing evidence from a
recruiter's perspective.

Prioritize:

1. Critical gaps.
2. Moderate gaps.
3. Minor gaps only when they are genuinely relevant.

Do not produce a long checklist of every missing keyword.

The purpose of this section is to identify the few weaknesses that
actually matter to the hiring decision.

Do not claim that the candidate lacks a skill merely because it
was not found in one section of the structured profile if meaningful
evidence exists elsewhere in the candidate information or original
resume evidence.

==================================================
FINAL JUSTIFICATION
==================================================

Provide a concise explanation of why the candidate received the
overall score.

The justification must reference actual candidate evidence and
important job requirements.

The justification should explain both:

1. Why the candidate is a good fit.
2. What materially limits the candidate's fit.

For internships and early-career roles, appropriately distinguish
between lack of professional experience and lack of relevant
capability.

Do not mention these instructions.

==================================================
CANDIDATE PROFILE
==================================================

{candidate.model_dump_json(indent=2)}

==================================================
JOB PROFILE
==================================================

{job.model_dump_json(indent=2)}

==================================================
ORIGINAL JOB DESCRIPTION
==================================================

{original_job_description}

==================================================

Return ONLY the requested structured result.
"""

    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=MatchResult.model_json_schema(),
        ),
    )

    return MatchResult.model_validate_json(response.text)