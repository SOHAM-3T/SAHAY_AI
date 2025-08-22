#!/usr/bin/env python3
"""
Interactive test script for the AI Career Mentor
Run this to test the chatbot functionality in the terminal
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


def interactive_career_advisor():
    """Interactive career advisor in terminal"""
    print("🤖 AI-360 Career Mentor - Terminal Version")
    print("=" * 50)

    try:
        # Import components
        from utils.pdf_parser import extract_text_from_pdf
        from utils.resume_parser import parse_resume
        from chatbot.career_bot import CareerBot

        # Check if resume exists
        resume_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "Resume.pdf"
        )
        if not os.path.exists(resume_path):
            print("❌ Resume not found at ../data/Resume.pdf")
            print("💡 Please make sure you have a Resume.pdf file in the data folder")
            return

        print("📄 Resume found! Initializing Career Bot...")

        # Initialize career bot
        career_bot = CareerBot(resume_path)
        print("✅ Career Bot initialized successfully!")

        # Show resume summary
        resume_data = career_bot.resume_data
        print(f"\n📋 Resume Summary:")
        print(f"   🛠️ Skills: {len(resume_data['skills'])}")
        print(f"   🚀 Projects: {len(resume_data['projects'])}")
        print(f"   💼 Experience: {len(resume_data['experience'])}")
        print(f"   📚 Education: {len(resume_data['education'])}")

        if resume_data["skills"]:
            print(f"\n🛠️ Your skills: {', '.join(resume_data['skills'][:10])}")

        # Interactive menu
        while True:
            print("\n" + "=" * 50)
            print("🎯 What would you like to do?")
            print("1. Analyze skills gap for a specific role")
            print("2. Get career path suggestions")
            print("3. Ask a career question")
            print("4. Exit")

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                # Skills gap analysis
                print("\n🔍 Skills Gap Analysis")
                print(
                    "Available roles: Data Scientist, Software Engineer, Product Manager, Data Analyst, ML Engineer"
                )
                target_role = input("Enter target role: ").strip()

                if target_role:
                    try:
                        analysis = career_bot.suggest_skills(target_role)
                        print(f"\n🎯 Analysis for {analysis['target_role']}:")
                        print(
                            f"✅ Your current skills: {len(analysis['current_skills'])}"
                        )
                        print(
                            f"📚 Skills to develop: {len(analysis['missing_skills'])}"
                        )

                        if analysis["missing_skills"]:
                            print(
                                f"\n📚 Missing skills: {', '.join(analysis['missing_skills'])}"
                            )

                        if analysis["recommendations"]:
                            print(f"\n💡 Recommendations:")
                            for rec in analysis["recommendations"]:
                                print(f"   • {rec}")
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")

            elif choice == "2":
                # Career path suggestions
                print("\n🛤️ Career Path Suggestions")
                try:
                    career_paths = career_bot.get_career_path_suggestions()
                    print("Based on your skills, consider these career paths:")
                    for i, path in enumerate(career_paths, 1):
                        print(f"   {i}. {path}")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")

            elif choice == "3":
                # Career question
                print("\n💬 Ask a Career Question")
                question = input("Enter your question: ").strip()

                if question:
                    try:
                        print("🤔 Thinking...")
                        response = career_bot.get_career_advice(question)
                        print(f"\n💡 Answer: {response}")
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")

            elif choice == "4":
                print("\n👋 Thank you for using AI-360 Career Mentor!")
                print("🚀 Good luck with your career journey!")
                break

            else:
                print("❌ Invalid choice. Please enter 1-4.")

    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("💡 Make sure all required packages are installed")
        print("   Run: pip install -r requirements.txt")

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    interactive_career_advisor()
