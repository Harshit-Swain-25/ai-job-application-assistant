import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def analyze_resume_fit(
    resume_text: str,
    job_description: str,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY was not found. Check your .env file.")

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    client = genai.Client(api_key=api_key)

    
    prompt = f"""
    You are an assistant that helps users understand how their resume
    relates to a job description. Analyze the resume using only the
    information explicitly provided.

    Follow these rules:
    - Do not invent skills, qualifications, work experience, or personal details.
    - Support identified strengths with evidence from the resume.
    - List potential gaps based on the job description.
    - A missing keyword does not prove the candidate lacks that skill.
    - Clearly distinguish resume evidence from suggestions.
    - Do not rewrite the resume yet.
    - Do not assume facts that are not explicitly stated.
    - When evidence is unclear, say the resume does not provide enough information.
    - Do not claim a skill was used in a project unless the resume explicitly
      connects that skill to the project.
    - Always refer to the person as "the candidate". Do not use a personal
      name in the analysis, even if one appears in the resume.
    
    Use these sections:
    1. Relevant strengths (with resume evidence)
    2. Potential gaps or areas to clarify
    3. Practical recommendations

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """


    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
    except errors.APIError as error:
        status_code = getattr(error, "code", "unknown")
        raise RuntimeError(f"Gemini API request failed (HTTP {status_code}). "
        "Check the API error details in the terminal.") from error
    
    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text
