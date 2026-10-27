
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def generate_cover_letter(
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
    Write a concise, professional cover letter tailored to the supplied
    job description.

    Evidence and accuracy rules:
    - Use only information explicitly supported by the resume.
    - Do not invent skills, qualifications, projects, employment history,
      achievements, years of experience, or personal details.
    - Listing a skill alone does not prove professional experience,
      proficiency, or successful use of that skill.
    - When a skill is only listed, describe it as a skill listed on the
      resume. Do not claim demonstrated experience or proficiency.
    - Do not describe the candidate as an experienced or professional
      developer unless the resume provides supporting evidence.
    - Do not use a person's name from the resume in the letter.
    - Use [Your Name] as the signature.
    - Do not invent the employer's name, contact details, or job details.
    - Use placeholders such as [Hiring Manager] and [Company Name]
      when appropriate.
    - Connect resume evidence to job requirements without exaggeration.
    - If the resume lacks enough evidence for a claim, omit that claim.
    - Do not include explanations before or after the cover letter.

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
        raise RuntimeError("Gemini could not generate the cover letter. Please try again later.") from error

    if not response.text:
        raise ValueError("Gemini returned an empty cover letter.")

    return response.text


def generate_application_talking_points(
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
    Prepare practical talking points for a candidate applying for this job.

    Use these sections:
    1. Relevant skills supported by resume evidence
    2. Experience or projects worth highlighting
    3. Job requirements to clarify or develop
    4. Questions the candidate should answer before finalizing the application

    Rules:
    - Use only facts explicitly supported by the resume.
    - Do not invent skills, projects, qualifications, or achievements.
    - Do not assume a missing resume keyword means the candidate lacks that skill.
    - Do not invent the candidate's name or personal details.
    - Clearly distinguish documented evidence from suggestions.
    - If the resume lacks relevant information, say so.

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
        raise RuntimeError("Gemini API error while generating talking points."
            f"(HTTP {error.code}): {error.message}") from error

    if not response.text:
        raise ValueError("Gemini returned empty application talking points.")

    return response.text
