import unittest
from unittest.mock import patch

from main import main


class TestMain(unittest.TestCase):
    @patch("builtins.input", side_effect=EOFError)
    @patch("builtins.print")
    def test_handles_interrupted_resume_path(self, mock_print, mock_input):
        main()
        mock_print.assert_any_call("\nResume input was interrupted. Please try again.")

    
    @patch("main.get_job_description")
    @patch("builtins.print")
    @patch("builtins.input", return_value="missing_resume.pdf")
    def test_invalid_resume_path_stops_application(self, mock_input, mock_print, mock_get_job_description):
        main()
        mock_print.assert_any_call("\nError loading resume: Resume file not found: missing_resume.pdf")
        mock_get_job_description.assert_not_called()

    
    @patch("main.generate_application_talking_points", return_value="Sample talking points")
    @patch("main.generate_cover_letter", return_value="Sample cover letter")
    @patch("main.analyze_resume_fit", return_value="Sample AI analysis")
    @patch("main.compare_skills", return_value={"matched_skills": ["Python"],"missing_skills": ["SQL"],})

    @patch("main.get_job_description", return_value="Python Developer")
    @patch("main.extract_resume_text", return_value="Python developer resume")
    @patch("builtins.print")
    @patch("builtins.input", return_value="sample_resume.pdf")
    def test_successful_application_flow(self, mock_input, mock_print, mock_extract_resume,
        mock_get_job_description,
        mock_compare_skills,
        mock_analyze_resume,
        mock_generate_cover_letter,
        mock_generate_talking_points,
    ):
        main()

        mock_extract_resume.assert_called_once_with("sample_resume.pdf")
        mock_get_job_description.assert_called_once_with()
        mock_compare_skills.assert_called_once()
        mock_analyze_resume.assert_called_once()
        mock_generate_cover_letter.assert_called_once()
        mock_generate_talking_points.assert_called_once()

        printed_text = "\n".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Sample AI analysis", printed_text)
        self.assertIn("Sample cover letter", printed_text)
        self.assertIn("Sample talking points", printed_text)



if __name__ == "__main__":
    unittest.main()