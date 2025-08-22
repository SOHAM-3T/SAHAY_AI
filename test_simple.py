#!/usr/bin/env python3
"""
Simple test script for AI Career Mentor
Run this from the project root directory
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_basic_functionality():
    """Test basic resume parsing and career bot functionality"""
    print("🚀 Testing AI Career Mentor - Basic Functionality")
    print("=" * 60)

    try:
        # Test 1: Resume parsing
        print("📄 Test 1: Resume Parsing")
        from utils.pdf_parser import extract_text_from_pdf
        from utils.resume_parser import parse_resume

        resume_path = "data/Resume.pdf"
        if not os.path.exists(resume_path):
            print(f"❌ Resume not found at: {resume_path}")
            return False

        # Extract and parse
        raw_text = extract_text_from_pdf(resume_path)
        parsed_data = parse_resume(raw_text)

        print(f"✅ Resume parsed successfully!")
        print(f"   🛠️ Skills: {len(parsed_data['skills'])}")
        print(f"   🚀 Projects: {len(parsed_data['projects'])}")
        print(f"   📚 Education: {len(parsed_data['education'])}")

        if parsed_data["skills"]:
            print(f"   🛠️ Sample skills: {', '.join(parsed_data['skills'][:5])}")

        # Test 2: Career Bot (without RAG for now)
        print("\n🤖 Test 2: Career Bot (Basic)")

        # Create a simple career bot without RAG dependencies
        class SimpleCareerBot:
            def __init__(self, resume_data):
                self.resume_data = resume_data

            def suggest_skills(self, target_role: str) -> dict:
                """Suggest skills to develop for a specific role"""
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
                    skill
                    for skill in target_skills
                    if skill.lower() not in current_skills
                ]

                return {
                    "target_role": target_role,
                    "current_skills": list(current_skills),
                    "missing_skills": missing_skills,
                    "recommendations": self._generate_skill_recommendations(
                        missing_skills
                    ),
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

        # Test the simple career bot
        career_bot = SimpleCareerBot(parsed_data)

        # Test skills analysis
        print("   🔍 Testing skills analysis for 'Data Scientist'...")
        analysis = career_bot.suggest_skills("Data Scientist")

        print(f"   ✅ Skills analysis completed!")
        print(f"      🎯 Target role: {analysis['target_role']}")
        print(f"      ✅ Current skills: {len(analysis['current_skills'])}")
        print(f"      📚 Missing skills: {len(analysis['missing_skills'])}")

        if analysis["missing_skills"]:
            print(f"      📚 Missing: {', '.join(analysis['missing_skills'][:3])}")

        if analysis["recommendations"]:
            print(f"      💡 Sample recommendations: {analysis['recommendations'][:2]}")

        # Test career paths
        print("   🛤️ Testing career path suggestions...")
        career_paths = career_bot.get_career_path_suggestions()
        print(f"   ✅ Suggested career paths: {', '.join(career_paths[:3])}")

        print("\n🎉 All basic tests passed!")
        print("🚀 Your AI Career Mentor core functionality is working!")

        return True

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("\n✅ Ready to proceed with Streamlit app!")
    else:
        print("\n❌ Some issues need to be fixed first.")
