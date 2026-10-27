
# AI Job Application Assistant

A beginner-friendly Python application that helps job seekers understand how their resume aligns with a job description and prepare application materials using Google's Gemini API.

## Features

- **Resume Parsing:** Extract text from PDF and DOCX resumes.
- **Skill Matching:** Identify selected technical skills in a resume and job description.
- **AI-Powered Resume Analysis:** Generate feedback on resume alignment with a job description.
- **Tailored Cover Letter:** Draft a cover letter based on the provided resume and job description.
- **Application Talking Points:** Generate evidence-based points to help prepare for an application or interview.
- **Streamlit Interface:** Use the application through a browser.
- **Command-Line Interface:** Run the application from the terminal.
- **Automated Tests:** Validate core functionality and error handling.

## Tech Stack

- Python
- Google Gemini API (`google-genai`)
- Streamlit
- pypdf
- python-docx
- python-dotenv
- unittest
- Ruff

## Project Structure

```text
ai-job-application-assistant/
├── app.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
├── tests/
└── data/
    └── sample_resumes/
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Harshit-Swain-25/ai-job-application-assistant.git
cd ai-job-application-assistant
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a local `.env` file in the project root using `.env.example` as a guide.

Add your own API key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own key. Never commit `.env` or share your API key publicly.

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

Follow the local URL printed in the terminal to open the application in your browser.

### 6. Run the command-line application

```bash
python main.py
```

### 7. Run automated tests

```bash
python -m unittest discover -s tests -v
```

### 8. Run Ruff

```bash
python -m ruff check .
```

## Important Notes

- AI-generated analysis and application materials should be reviewed and edited before use.
- Skill matching is based on selected keywords and does not represent a complete assessment of a candidate's abilities.
- AI output may be inaccurate or incomplete. Do not rely on generated content without reviewing it.
- Gemini API access, quotas, availability, and costs depend on the applicable Google account and API terms.
- The included sample resumes are fictional examples for testing.
- Avoid uploading confidential or sensitive personal information unless you understand the service's data-handling terms.

## Future Improvements

- Support additional resume formats.
- Expand skill matching and customization.
- Improve the presentation and export of generated application materials.
- Add more test cases as the application evolves.

## License

No license has been specified yet. All rights are reserved unless a license is added to this repository.
