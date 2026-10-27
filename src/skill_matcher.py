import re


def _contains_skill(text: str, skill: str) -> bool:
    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def compare_skills(
        skills: list[str],
        resume_text: str,
        job_description: str,
) -> dict[str, list[str]]:
    matched_skills = []
    missing_skills = []

    for skill in skills:
        skill_clean = skill.lower().strip()
        if not skill_clean:
            continue

        in_resume = _contains_skill(resume_text, skill_clean)
        in_job_description = _contains_skill(job_description, skill_clean)

        if in_resume and in_job_description:
            matched_skills.append(skill)
        elif in_job_description and not in_resume:
            missing_skills.append(skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }