#!/usr/bin/env python3
"""
AI-360 Career Mentor - Terminal Version
A powerful career advisor that analyzes resumes and provides personalized guidance
"""

import os
import sys
import time
from typing import Dict, List

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from utils.pdf_parser import extract_text_from_pdf
from utils.resume_parser import parse_resume


class CareerMentor:
    def __init__(self):
        self.resume_data = None
        self.career_bot = None

    def load_resume(self, resume_path: str) -> bool:
        """Load and parse a resume"""
        try:
            print("📄 Loading resume...")
            raw_text = extract_text_from_pdf(resume_path)
            self.resume_data = parse_resume(raw_text)

            print("✅ Resume loaded successfully!")
            self._display_resume_summary()

            # Initialize career bot
            self.career_bot = self._create_career_bot()
            return True

        except Exception as e:
            print(f"❌ Error loading resume: {str(e)}")
            return False

    def _display_resume_summary(self):
        """Display a summary of the parsed resume"""
        print("\n" + "=" * 60)
        print("📋 RESUME SUMMARY")
        print("=" * 60)

        data = self.resume_data
        print(f"🛠️  Skills: {len(data['skills'])}")
        print(f"🚀 Projects: {len(data['projects'])}")
        print(f"📚 Education: {len(data['education'])}")
        print(f"💼 Experience: {len(data['experience'])}")

        if data["skills"]:
            print(f"\n🛠️  Top Skills: {', '.join(data['skills'][:8])}")

        if data["education"]:
            print(f"📚 Education: {data['education'][0]}")

    def _create_career_bot(self):
        """Create the career bot with all functionality"""

        class CareerBot:
            def __init__(self, resume_data):
                self.resume_data = resume_data

            def suggest_skills(self, target_role: str) -> Dict:
                """Suggest skills to develop for a specific role"""
                role_skills = {
                    "data scientist": [
                        "Python",
                        "SQL",
                        "Machine Learning",
                        "Statistics",
                        "Data Visualization",
                        "Deep Learning",
                        "NLP",
                    ],
                    "software engineer": [
                        "Programming",
                        "Data Structures",
                        "Algorithms",
                        "System Design",
                        "Testing",
                        "Git",
                        "Docker",
                    ],
                    "product manager": [
                        "Product Strategy",
                        "User Research",
                        "Data Analysis",
                        "Leadership",
                        "Agile",
                        "Market Analysis",
                    ],
                    "data analyst": [
                        "SQL",
                        "Excel",
                        "Python",
                        "Data Visualization",
                        "Statistical Analysis",
                        "Business Intelligence",
                    ],
                    "ml engineer": [
                        "Python",
                        "Machine Learning",
                        "Deep Learning",
                        "MLOps",
                        "Data Engineering",
                        "TensorFlow",
                        "PyTorch",
                    ],
                    "full stack developer": [
                        "JavaScript",
                        "React",
                        "Node.js",
                        "Python",
                        "Database Design",
                        "API Development",
                    ],
                    "devops engineer": [
                        "Linux",
                        "Docker",
                        "Kubernetes",
                        "CI/CD",
                        "Cloud Platforms",
                        "Infrastructure as Code",
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

            def _generate_skill_recommendations(
                self, missing_skills: List[str]
            ) -> List[str]:
                """Generate specific recommendations for missing skills"""
                recommendations = []
                for skill in missing_skills:
                    if "python" in skill.lower():
                        recommendations.append(
                            f"🐍 Learn {skill}: Start with Codecademy or freeCodeCamp Python courses"
                        )
                    elif "sql" in skill.lower():
                        recommendations.append(
                            f"🗄️ Learn {skill}: Practice on LeetCode or HackerRank SQL challenges"
                        )
                    elif "machine learning" in skill.lower():
                        recommendations.append(
                            f"🤖 Learn {skill}: Take Andrew Ng's ML course on Coursera"
                        )
                    elif "statistics" in skill.lower():
                        recommendations.append(
                            f"📊 Learn {skill}: Take Statistics courses on Khan Academy or edX"
                        )
                    elif "data visualization" in skill.lower():
                        recommendations.append(
                            f"📈 Learn {skill}: Master Tableau, Power BI, or Python libraries like Matplotlib"
                        )
                    elif "react" in skill.lower():
                        recommendations.append(
                            f"⚛️ Learn {skill}: Complete React tutorials on React.dev and build projects"
                        )
                    elif "docker" in skill.lower():
                        recommendations.append(
                            f"🐳 Learn {skill}: Follow Docker's official tutorials and practice with containers"
                        )
                    else:
                        recommendations.append(
                            f"📚 Develop {skill}: Research online courses and practice projects"
                        )

                return recommendations

            def get_career_path_suggestions(self) -> List[str]:
                """Suggest potential career paths based on current skills"""
                skills = set(self.resume_data["skills"])

                career_paths = []
                if any("python" in skill.lower() for skill in skills):
                    career_paths.append("Data Scientist")
                    career_paths.append("Software Engineer")
                    career_paths.append("ML Engineer")
                if any("java" in skill.lower() for skill in skills):
                    career_paths.append("Java Developer")
                    career_paths.append("Android Developer")
                    career_paths.append("Enterprise Developer")
                if any("sql" in skill.lower() for skill in skills):
                    career_paths.append("Data Analyst")
                    career_paths.append("Business Intelligence Developer")
                if any("machine learning" in skill.lower() for skill in skills):
                    career_paths.append("AI Researcher")
                    career_paths.append("ML Engineer")
                if any(
                    "web" in skill.lower() or "html" in skill.lower()
                    for skill in skills
                ):
                    career_paths.append("Frontend Developer")
                    career_paths.append("Full Stack Developer")

                return career_paths or [
                    "General Software Developer",
                    "IT Consultant",
                    "Tech Support",
                ]

            def get_career_advice(self, question: str) -> str:
                """Provide career advice based on the question"""
                question_lower = question.lower()

                if "skill" in question_lower and "gap" in question_lower:
                    return "I can help you analyze skills gaps! Use the 'Skills Gap Analysis' feature to see what skills you need for your target role."

                elif "career" in question_lower and "path" in question_lower:
                    return "Great question! Use 'Career Path Suggestions' to see what career paths align with your current skills and background."

                elif "resume" in question_lower:
                    return f"Your resume shows {len(self.resume_data['skills'])} skills, {len(self.resume_data['projects'])} projects, and {len(self.resume_data['education'])} education items. You're well-positioned for tech roles!"

                elif "python" in question_lower:
                    if any(
                        "python" in skill.lower()
                        for skill in self.resume_data["skills"]
                    ):
                        return "Great! You already have Python skills. Consider building more projects and learning advanced topics like Django, Flask, or data science libraries."
                    else:
                        return "Python is a great skill to add! Start with basic syntax, then move to web development or data science depending on your interests."

                elif "interview" in question_lower:
                    return "For tech interviews, focus on: 1) Data Structures & Algorithms practice on LeetCode, 2) System Design concepts, 3) Your projects and experience, 4) Behavioral questions using STAR method."

                elif "salary" in question_lower or "pay" in question_lower:
                    return "Salary varies by location, experience, and company. Research on Glassdoor, Levels.fyi, or LinkedIn. Focus on building skills first - good compensation follows expertise."

                else:
                    return "I'm here to help with your career! You can ask me about skills, career paths, resume improvement, interview prep, or use the interactive features above."

        return CareerBot(self.resume_data)

    def run(self):
        """Main application loop"""
        self._show_welcome()

        # Load resume
        resume_path = "data/Resume.pdf"
        if not os.path.exists(resume_path):
            print(f"❌ Resume not found at: {resume_path}")
            print("💡 Please make sure you have a Resume.pdf file in the data folder")
            return

        if not self.load_resume(resume_path):
            return

        # Main menu loop
        while True:
            self._show_main_menu()
            choice = input("\n🎯 Enter your choice (1-6): ").strip()

            if choice == "1":
                self._skills_gap_analysis()
            elif choice == "2":
                self._career_path_suggestions()
            elif choice == "3":
                self._resume_insights()
            elif choice == "4":
                self._career_advice()
            elif choice == "5":
                self._learning_roadmap()
            elif choice == "6":
                self._goodbye()
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")

            input("\n⏸️  Press Enter to continue...")

    def _show_welcome(self):
        """Show welcome message"""
        print("\n" + "=" * 70)
        print("🤖 AI-360 CAREER MENTOR")
        print("=" * 70)
        print("Your AI-powered career advisor that analyzes resumes and provides")
        print("personalized guidance for your professional development journey!")
        print("=" * 70)
        time.sleep(1)

    def _show_main_menu(self):
        """Show the main menu"""
        print("\n" + "=" * 60)
        print("🎯 MAIN MENU")
        print("=" * 60)
        print("1. 🔍 Skills Gap Analysis")
        print("2. 🛤️  Career Path Suggestions")
        print("3. 📋 Resume Insights & Strengths")
        print("4. 💬 Ask Career Questions")
        print("5. 🗺️  Learning Roadmap")
        print("6. 👋 Exit")
        print("=" * 60)

    def _skills_gap_analysis(self):
        """Perform skills gap analysis"""
        print("\n🔍 SKILLS GAP ANALYSIS")
        print("-" * 40)

        print("Available roles:")
        roles = [
            "Data Scientist",
            "Software Engineer",
            "Product Manager",
            "Data Analyst",
            "ML Engineer",
            "Full Stack Developer",
            "DevOps Engineer",
        ]

        for i, role in enumerate(roles, 1):
            print(f"   {i}. {role}")

        try:
            choice = int(input("\nSelect role number: ")) - 1
            if 0 <= choice < len(roles):
                target_role = roles[choice]
                self._analyze_skills_for_role(target_role)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a valid number.")

    def _analyze_skills_for_role(self, target_role: str):
        """Analyze skills for a specific role"""
        print(f"\n🎯 Analyzing skills for: {target_role}")
        print("-" * 50)

        analysis = self.career_bot.suggest_skills(target_role)

        print(f"✅ Your current skills: {len(analysis['current_skills'])}")
        print(f"📚 Skills to develop: {len(analysis['missing_skills'])}")

        if analysis["missing_skills"]:
            print(f"\n📚 Missing skills for {target_role}:")
            for skill in analysis["missing_skills"]:
                print(f"   • {skill}")

        if analysis["recommendations"]:
            print(f"\n💡 Learning Recommendations:")
            for rec in analysis["recommendations"]:
                print(f"   {rec}")

        # Show progress
        current_count = len(analysis["current_skills"])
        missing_count = len(analysis["missing_skills"])
        total_required = current_count + missing_count
        progress = current_count / total_required if total_required > 0 else 0

        print(
            f"\n📊 Progress: {current_count}/{total_required} skills ({progress:.1%})"
        )

        # Visual progress bar
        bar_length = 30
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        print(f"[{bar}] {progress:.1%}")

    def _career_path_suggestions(self):
        """Show career path suggestions"""
        print("\n🛤️  CAREER PATH SUGGESTIONS")
        print("-" * 40)

        career_paths = self.career_bot.get_career_path_suggestions()

        print("Based on your skills, consider these career paths:")
        for i, path in enumerate(career_paths, 1):
            print(f"   {i}. {path}")

        # Show skill alignment
        if career_paths:
            print(f"\n🎯 Why These Paths Fit You:")
            skills = set(self.resume_data["skills"])

            if any("python" in skill.lower() for skill in skills):
                print(
                    "   ✅ Python Skills: Great for Data Science, Software Engineering, and ML"
                )
            if any("java" in skill.lower() for skill in skills):
                print(
                    "   ✅ Java Skills: Perfect for Enterprise Software and Android Development"
                )
            if any("sql" in skill.lower() for skill in skills):
                print(
                    "   ✅ SQL Skills: Essential for Data Analysis and Business Intelligence"
                )
            if any("machine learning" in skill.lower() for skill in skills):
                print("   ✅ ML Skills: Excellent for AI/ML Engineering and Research")

    def _resume_insights(self):
        """Show detailed resume insights"""
        print("\n📋 RESUME INSIGHTS & STRENGTHS")
        print("-" * 40)

        data = self.resume_data

        print(f"🛠️  Skills Analysis:")
        print(f"   Total Skills: {len(data['skills'])}")
        if data["skills"]:
            print(f"   Top Technical Skills: {', '.join(data['skills'][:10])}")

        print(f"\n🚀 Project Portfolio:")
        print(f"   Total Projects: {len(data['projects'])}")
        if data["projects"]:
            print(f"   Sample Projects: {', '.join(data['projects'][:3])}")

        print(f"\n📚 Educational Background:")
        print(f"   Total Education Items: {len(data['education'])}")
        if data["education"]:
            for edu in data["education"]:
                print(f"   • {edu}")

        print(f"\n💼 Experience:")
        print(f"   Total Experience Items: {len(data['experience'])}")
        if data["experience"]:
            for exp in data["experience"]:
                print(f"   • {exp}")

    def _career_advice(self):
        """Interactive career advice"""
        print("\n💬 CAREER ADVICE")
        print("-" * 40)
        print("Ask me anything about your career, skills, or job search!")
        print("Type 'menu' to return to main menu.")

        while True:
            question = input("\n❓ Your question: ").strip()

            if question.lower() == "menu":
                break

            if question:
                print("\n💡 Answer:")
                answer = self.career_bot.get_career_advice(question)
                print(f"   {answer}")
            else:
                print("❌ Please enter a question.")

    def _learning_roadmap(self):
        """Show learning roadmap"""
        print("\n🗺️  LEARNING ROADMAP")
        print("-" * 40)

        print("Based on your current skills, here's a suggested learning path:")

        skills = set(self.resume_data["skills"])

        if any("python" in skill.lower() for skill in skills):
            print("\n🐍 Python Development Path:")
            print("   1. Advanced Python (Decorators, Generators)")
            print("   2. Web Development (Django/Flask)")
            print("   3. Data Science Libraries (Pandas, NumPy)")
            print("   4. Machine Learning (Scikit-learn)")

        if any("java" in skill.lower() for skill in skills):
            print("\n☕ Java Development Path:")
            print("   1. Advanced Java (Collections, Streams)")
            print("   2. Spring Framework")
            print("   3. Microservices Architecture")
            print("   4. Cloud Deployment (AWS/Azure)")

        if any("sql" in skill.lower() for skill in skills):
            print("\n🗄️  Data Analysis Path:")
            print("   1. Advanced SQL (Window Functions)")
            print("   2. Data Visualization (Tableau, Power BI)")
            print("   3. Business Intelligence")
            print("   4. Data Engineering")

        print("\n🎯 General Career Development:")
        print("   1. Build portfolio projects")
        print("   2. Contribute to open source")
        print("   3. Network and attend tech meetups")
        print("   4. Stay updated with industry trends")

    def _goodbye(self):
        """Show goodbye message"""
        print("\n" + "=" * 60)
        print("👋 Thank you for using AI-360 Career Mentor!")
        print("🚀 Good luck with your career journey!")
        print("💡 Remember: Continuous learning is the key to success!")
        print("=" * 60)


def main():
    """Main entry point"""
    try:
        mentor = CareerMentor()
        mentor.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using AI-360 Career Mentor!")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
