from src.application_writer import (
    generate_application_talking_points,
    generate_cover_letter,
)
from src.job_description import get_job_description
from src.llm_analyzer import analyze_resume_fit
from src.resume_parser import extract_resume_text
from src.skill_matcher import compare_skills


def main():
    print("AI Job Application Assistant")
    print("-" * 32)
 
    try: 
        resume_path = input("Enter the path to your resume (PDF or DOCX): ").strip()
    except EOFError:
        print("\nResume input was interrupted. Please try again.")
        return
    
    try:
        resume_text = extract_resume_text(resume_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"\nError loading resume: {error}")
        return
    
    try:
        job_description = get_job_description()
    except ValueError as error:
        print(f"\nError: {error}")
        return
    
    skills = ["Python", "pandas", "Git", "SQL", "data analysis"]
    results = compare_skills(skills, resume_text, job_description)

    print("\nResume-to-Job Comparison Summary")
    print("=" * 34)

    print("\nMatched skills:")
    if results["matched_skills"]:
        for skill in results["matched_skills"]:
            print(f"- {skill}")
    else:
        print("- No matched skills found.")

    print("\nPotentially missing skills:")
    if results["missing_skills"]:
        for skill in results["missing_skills"]:
            print(f"- {skill}")
    else:
        print("- No potential skill gaps found.")

    print("\nImportant limitation:")
    print("This is a basic keyword comparison, not a complete measure of your suitability for the role.")
    
    print("A skill not found in your resume text may still be one you possess.")

    try:
        ai_analysis = analyze_resume_fit(resume_text, job_description)
    except (ValueError, RuntimeError) as error:  
        print(f"\nAI analysis could not be completed: {error}")
        ai_analysis = None    
    else:
        print("\nAI-Powered Resume Analysis")
        print("=" * 29)
        print(ai_analysis)
    
    try:
        cover_letter = generate_cover_letter(resume_text, job_description)
    except (ValueError, RuntimeError) as error:
        print(f"\nCover letter generation could not be completed: {error}")
    else:
        print("\nTailored Cover Letter")
        print("=" * 23)
        print(cover_letter)

    try:
        talking_points = generate_application_talking_points(resume_text, job_description)
    except (ValueError, RuntimeError) as error:
        print(f"\nApplication talking points could not be generated: {error}")
    else:
        print("\nApplication Talking Points")
        print("=" * 27)
        print(talking_points)



if __name__ == "__main__":
    main()
