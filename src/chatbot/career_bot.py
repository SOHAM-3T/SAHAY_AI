from ..rag.rag_pipeline import CareerRAGPipeline
from ..utils.resume_parser import parse_resume
from ..utils.pdf_parser import extract_text_from_pdf
import re


class CareerBot:
    def __init__(self, resume_path: str):
        self.resume_path = resume_path
        self.rag_pipeline = CareerRAGPipeline(resume_path)
        self.resume_data = self._parse_resume()

    def _parse_resume(self):
        """Parse and store resume data"""
        raw_text = extract_text_from_pdf(self.resume_path)
        return parse_resume(raw_text)

    def get_career_advice(self, question: str) -> str:
        """Get personalized career advice"""
        response = self.rag_pipeline.get_career_advice(question)
        return response.get(
            "answer", "I couldn't provide specific advice for that question."
        )

    def suggest_skills(self, target_role: str) -> dict:
        """Suggest skills to develop for a specific role"""
        # Common skills for different roles
        role_skills = {
            "data scientist": [
                "Python",
                "SQL",
                "Machine Learning",
                "Statistics",
                "Data Visualization",
            ],
            "software engineer": [
                "Programming",
                "Data Structures",
                "Algorithms",
                "System Design",
                "Testing",
            ],
            "product manager": [
                "Product Strategy",
                "User Research",
                "Data Analysis",
                "Leadership",
                "Agile",
            ],
            "data analyst": [
                "SQL",
                "Excel",
                "Python",
                "Data Visualization",
                "Statistical Analysis",
            ],
        }

        target_skills = role_skills.get(target_role.lower(), [])
        current_skills = set(self.resume_data["skills"])

        # Find missing skills
        missing_skills = [
            skill for skill in target_skills if skill.lower() not in current_skills
        ]

        return {
            "target_role": target_role,
            "current_skills": list(current_skills),
            "missing_skills": missing_skills,
            "recommendations": self._generate_skill_recommendations(missing_skills),
        }

    def _generate_skill_recommendations(self, missing_skills: list) -> list:
        """Generate specific recommendations for missing skills"""
        recommendations = []
        for skill in missing_skills:
            if "python" in skill.lower():
                recommendations.append(
                    f"Learn {skill}: Start with Codecademy or freeCodeCamp Python courses"
                )
            elif "sql" in skill.lower():
                recommendations.append(
                    f"Learn {skill}: Practice on LeetCode or HackerRank SQL challenges"
                )
            elif "machine learning" in skill.lower():
                recommendations.append(
                    f"Learn {skill}: Take Andrew Ng's ML course on Coursera"
                )
            else:
                recommendations.append(
                    f"Develop {skill}: Research online courses and practice projects"
                )

        return recommendations

    def get_career_path_suggestions(self) -> list:
        """Suggest potential career paths based on current skills"""
        skills = set(self.resume_data["skills"])

        career_paths = []
        if any("python" in skill.lower() for skill in skills):
            career_paths.append("Data Scientist")
            career_paths.append("Software Engineer")
        if any("sql" in skill.lower() for skill in skills):
            career_paths.append("Data Analyst")
            career_paths.append("Business Intelligence Developer")
        if any("machine learning" in skill.lower() for skill in skills):
            career_paths.append("ML Engineer")
            career_paths.append("AI Researcher")

        return career_paths or ["General Software Developer", "IT Consultant"]
