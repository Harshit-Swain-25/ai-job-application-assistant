import tempfile
import unittest
from pathlib import Path

from src.resume_parser import extract_resume_text


class TestResumeParser(unittest.TestCase):
    def test_extract_text_from_docx(self):
        text = extract_resume_text(
            "data/sample_resumes/sample_resume.docx"
        )

        self.assertIn("Alex Morgan", text)
        self.assertIn("Python", text)

    def test_extract_text_from_pdf(self):
        text = extract_resume_text(
            "data/sample_resumes/sample_resume.pdf"
        )

        self.assertIn("Alex Morgan", text)
        self.assertIn("Python Developer", text)

    def test_missing_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            extract_resume_text(
                "data/sample_resumes/missing_resume.docx"
            )

    def test_unsupported_file_type_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "resume.txt"
            file_path.write_text("Test content", encoding="utf-8")

            with self.assertRaises(ValueError):
                extract_resume_text(str(file_path))

    def test_empty_docx_raises_error(self):
        with self.assertRaisesRegex(ValueError, "No readable text found"):
            extract_resume_text(
                "data/sample_resumes/empty_resume.docx"
            )

    def test_corrupted_pdf_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "corrupted_resume.pdf"
            file_path.write_text("This is not a valid PDF.", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Could not read the resume"):
                extract_resume_text(str(file_path))
    


if __name__ == "__main__":
    unittest.main()
