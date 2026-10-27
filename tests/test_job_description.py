
import unittest
from unittest.mock import patch

from src.job_description import get_job_description


class TestJobDescription(unittest.TestCase):
    @patch("builtins.input", side_effect=["Python Developer","Skills: Python, pandas, Git","",])
    def test_collects_multiple_lines(self, mock_input):
        result = get_job_description()

        self.assertIn("Python Developer", result)
        self.assertIn("Skills: Python, pandas, Git", result)
        self.assertEqual(result, "Python Developer\nSkills: Python, pandas, Git",)

    @patch("builtins.input", side_effect=["",])
    def test_rejects_empty_description(self, mock_input):
        with self.assertRaisesRegex(ValueError, "Job description cannot be empty"):
            get_job_description()
    
    @patch("builtins.input", side_effect=EOFError)
    def test_handles_interrupted_input(self, mock_input):
        with self.assertRaisesRegex(ValueError, "Job description input was interrupted"):
            get_job_description()


if __name__ == "__main__":
    unittest.main()
