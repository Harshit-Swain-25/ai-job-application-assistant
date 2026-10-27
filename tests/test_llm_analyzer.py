
import unittest
from unittest.mock import Mock, patch

from src.llm_analyzer import analyze_resume_fit


class TestLLMAnalyzer(unittest.TestCase):
    def setUp(self):
        self.resume = ("Python developer with experience using Python, pandas, and Git.")
        self.job_description = "Python Developer requiring Python and SQL."

    def test_rejects_empty_resume(self):
        with self.assertRaises(ValueError):
            analyze_resume_fit("", self.job_description)

    def test_rejects_empty_job_description(self):
        with self.assertRaises(ValueError):
            analyze_resume_fit(self.resume, "")

    @patch("src.llm_analyzer.genai.Client")
    def test_returns_gemini_analysis(self, mock_client_class):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "Relevant strengths: Python and pandas."

        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            result = analyze_resume_fit(
                self.resume,
                self.job_description,
            )

        self.assertEqual(
            result,
            "Relevant strengths: Python and pandas.",
        )
        mock_client.models.generate_content.assert_called_once()

    
    
    @patch("src.llm_analyzer.genai.Client")
    def test_rejects_empty_gemini_response(self, mock_client_class):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = None

        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        
        with (
            patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}),
            self.assertRaises(ValueError),
        ):
            analyze_resume_fit(
                self.resume,
                self.job_description,
            )
    

    @patch("src.llm_analyzer.genai.Client")
    def test_handles_gemini_api_error(self, mock_client_class):
        from google.genai import errors

        mock_client = Mock()
        mock_client.models.generate_content.side_effect = (
            errors.APIError(
                503,
                {"message": "Temporary service error"},
            )
        )
        mock_client_class.return_value = mock_client

        with (
            patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}),
            self.assertRaisesRegex(
                RuntimeError,
                "Gemini API request failed",
            ),
        ):
            analyze_resume_fit(
                self.resume,
                self.job_description,
            )


if __name__ == "__main__":
    unittest.main()
