import os
import unittest
from unittest.mock import Mock, patch

from google.genai import errors

from src.application_writer import (
    generate_application_talking_points,
    generate_cover_letter,
)


class TestApplicationWriter(unittest.TestCase):
    def setUp(self):
        self.resume = ("Python developer with experience using Python, pandas, and Git.")
        self.job_description = ("Python Developer requiring Python, pandas, Git, and SQL.")

    def test_cover_letter_rejects_empty_resume(self):
        with self.assertRaises(ValueError):
            generate_cover_letter("", self.job_description)

    def test_cover_letter_rejects_empty_job_description(self):
        with self.assertRaises(ValueError):
            generate_cover_letter(self.resume, "")

    def test_talking_points_reject_empty_resume(self):
        with self.assertRaises(ValueError):
            generate_application_talking_points("", self.job_description)

    def test_talking_points_reject_empty_job_description(self):
        with self.assertRaises(ValueError):
            generate_application_talking_points(self.resume, "")

    @patch("src.application_writer.genai.Client")
    def test_generates_cover_letter(self, mock_client_class):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "Dear Hiring Manager, I am applying for this role."
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            result = generate_cover_letter(
                self.resume,
                self.job_description,
            )

        self.assertEqual(result, "Dear Hiring Manager, I am applying for this role.",)
        mock_client.models.generate_content.assert_called_once()

    @patch("src.application_writer.genai.Client")
    def test_generates_application_talking_points(self, mock_client_class):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "Highlight the documented Python experience."
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            result = generate_application_talking_points(
                self.resume,
                self.job_description,
            )

        self.assertEqual(result, "Highlight the documented Python experience.",)
        mock_client.models.generate_content.assert_called_once()

    @patch("src.application_writer.genai.Client")
    def test_cover_letter_handles_api_error(self, mock_client_class):
        from google.genai import errors

        mock_client = Mock()
        mock_client.models.generate_content.side_effect = errors.APIError(
            503,
            {"message": "Temporary service error"},
        )
        mock_client_class.return_value = mock_client

        with (
            patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}),
            self.assertRaisesRegex(RuntimeError, "Gemini could not generate the cover letter",),
        ):
            generate_cover_letter(self.resume, self.job_description)

    
    def test_talking_points_handles_api_error(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}),patch("src.application_writer.genai.Client") as mock_client:
                mock_client.return_value.models.generate_content.side_effect = (
                    errors.APIError(503, {"message": "Temporary service error"},)
                )

                with self.assertRaisesRegex(RuntimeError, "Gemini API error while generating talking points",):
                    generate_application_talking_points(
                        "Python, pandas",
                        "Python Developer",
                    )

if __name__ == "__main__":
    unittest.main()
