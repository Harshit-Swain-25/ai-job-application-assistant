
import streamlit as st

from src.application_writer import (
    generate_application_talking_points,
    generate_cover_letter,
)
from src.llm_analyzer import analyze_resume_fit
from src.resume_parser import extract_resume_text
from src.skill_matcher import compare_skills


def extract_resume_text_from_upload(uploaded_file):
    import tempfile
    from pathlib import Path

    suffix = Path(uploaded_file.name).suffix.lower()

    with tempfile.NamedTemporaryFile(
        suffix=suffix,
        delete=False,
    ) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = Path(temp_file.name)

    try:
        return extract_resume_text(str(temp_path))
    finally:
        temp_path.unlink(missing_ok=True)

st.set_page_config(page_title="AI Job Application Assistant", page_icon="💼", layout="centered",)

st.title("💼 AI Job Application Assistant")
st.write("Analyze how your resume matches a job description and prepare for your application.")

st.subheader("1. Upload Your Resume")
uploaded_resume = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Upload a PDF or DOCX resume.",
)

st.subheader("2. Job Description")
job_description = st.text_area(
    "Paste the job description",
    height=250,
    placeholder="Paste the full job description here...",
)

analyze_button = st.button(
    "Analyze Application",
    type="primary",
    use_container_width=True,
)

if analyze_button:
    if uploaded_resume is None:
        st.error("Please upload your resume first.")

    elif not job_description.strip():
        st.error("Please enter the job description.")

    else:
        try:
            resume_text = extract_resume_text_from_upload(
                uploaded_resume
            )
        except (ValueError, OSError) as error:
            st.error(f"Could not read the resume: {error}")
        else:
            skills = ["Python", "pandas", "Git", "SQL", "data analysis",]

            results = compare_skills(skills, resume_text, job_description,)
            st.success("Resume and job description processed!")
            st.subheader("3. Resume-to-Job Comparison")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Matched skills**")
                if results["matched_skills"]:
                    for skill in results["matched_skills"]:
                        st.write(f"- {skill}")
                else:
                    st.write("No matched skills found.")

            with col2:
                st.markdown("**Potentially missing skills**")
                if results["missing_skills"]:
                    for skill in results["missing_skills"]:
                        st.write(f"- {skill}")
                else:
                    st.write("No potential skill gaps found.")

            st.caption("This is a basic keyword comparison, not a complete measure of your suitability. A skill not found in your resume may still be one you possess.")
            st.subheader("4. AI-Powered Resume Analysis")

            with st.spinner("Analyzing your resume with AI..."):
                try:
                    ai_analysis = analyze_resume_fit(resume_text, job_description,)
                    st.write(ai_analysis)
                except (ValueError, RuntimeError) as error:
                    st.error(f"AI analysis could not be completed: {error}")

            st.subheader("5. Tailored Cover Letter")

            with st.spinner("Generating your cover letter..."):
                try:
                    cover_letter = generate_cover_letter(
                        resume_text,
                        job_description,
                    )
                    st.write(cover_letter)
                except (ValueError, RuntimeError) as error:
                    st.error(f"Cover letter generation could not be completed: {error}")

            st.subheader("6. Application Talking Points")
            with st.spinner("Preparing application talking points..."):
                try:
                    talking_points = generate_application_talking_points(
                        resume_text,
                        job_description,
                    )
                    st.write(talking_points)
                except (ValueError, RuntimeError) as error:
                    st.error(
                        "Application talking points could not be generated: "
                        f"{error}"
                    )
