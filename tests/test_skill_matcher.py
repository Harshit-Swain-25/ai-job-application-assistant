
import unittest

from src.skill_matcher import compare_skills


class TestSkillMatcher(unittest.TestCase):
    def test_identifies_matched_and_missing_skills(self):
        skills = ["Python", "pandas", "Git", "SQL"]

        resume_text = "Python developer with pandas and Git experience."
        job_description = (
            "Looking for Python, pandas, Git, and SQL skills."
        )

        result = compare_skills(
            skills, resume_text, job_description
        )

        self.assertEqual(
            result["matched_skills"],
            ["Python", "pandas", "Git"],
        )
        self.assertEqual(
            result["missing_skills"],
            ["SQL"],
        )

    def test_matching_is_case_insensitive(self):
        result = compare_skills(
            ["PYTHON"],
            "Python developer",
            "python required",
        )

        self.assertEqual(result["matched_skills"], ["PYTHON"])
        self.assertEqual(result["missing_skills"], [])

    def test_ignores_empty_skill_names(self):
        result = compare_skills(
            ["", "   ", "Python"],
            "Python developer",
            "Python required",
        )

        self.assertEqual(result["matched_skills"], ["Python"])
        self.assertEqual(result["missing_skills"], [])

    
    def test_sql_does_not_match_nosql(self):
        result = compare_skills(
            ["SQL"],
            "Experienced with NoSQL databases",
            "SQL knowledge is required",
        )

        self.assertEqual(result["matched_skills"], [])
        self.assertEqual(result["missing_skills"], ["SQL"])



if __name__ == "__main__":
    unittest.main()
