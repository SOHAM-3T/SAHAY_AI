#!/usr/bin/env python3
"""
Test script for resume parser functionality
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.pdf_parser import extract_text_from_pdf
from utils.resume_parser import parse_resume


def test_resume_parsing():
    """Test the complete resume parsing pipeline"""
    print("🧪 Testing Resume Parser...")

    # Test with the resume in data folder
    resume_path = os.path.join(os.path.dirname(__file__), "..", "data", "Resume.pdf")

    if not os.path.exists(resume_path):
        print(f"❌ Resume not found at: {resume_path}")
        return False

    try:
        # Step 1: Extract text from PDF
        print("📄 Step 1: Extracting text from PDF...")
        raw_text = extract_text_from_pdf(resume_path)

        if not raw_text:
            print("❌ No text extracted from PDF")
            return False

        print(f"✅ Text extracted successfully! Length: {len(raw_text)} characters")
        print(f"📝 First 200 characters: {raw_text[:200]}...")

        # Step 2: Parse resume sections
        print("\n🔍 Step 2: Parsing resume sections...")
        parsed_data = parse_resume(raw_text)

        print("✅ Resume parsed successfully!")
        print(f"📚 Education: {len(parsed_data['education'])} items")
        print(f"💼 Experience: {len(parsed_data['experience'])} items")
        print(f"🚀 Projects: {len(parsed_data['projects'])} items")
        print(f"🛠️ Skills: {len(parsed_data['skills'])} items")

        # Show some sample data
        if parsed_data["skills"]:
            print(f"\n🛠️ Sample skills: {parsed_data['skills'][:5]}")

        if parsed_data["education"]:
            print(f"📚 Sample education: {parsed_data['education'][:2]}")

        return True

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_career_bot():
    """Test the career bot functionality"""
    print("\n🤖 Testing Career Bot...")

    try:
        from chatbot.career_bot import CareerBot

        # Test with resume
        resume_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "Resume.pdf"
        )
        if os.path.exists(resume_path):
            print("📄 Initializing Career Bot with resume...")
            career_bot = CareerBot(resume_path)

            print("✅ Career Bot initialized successfully!")

            # Test skills suggestion
            print("\n🔍 Testing skills suggestion...")
            skills_analysis = career_bot.suggest_skills("Data Scientist")

            print(f"✅ Skills analysis completed!")
            print(f"🎯 Target role: {skills_analysis['target_role']}")
            print(f"✅ Current skills: {len(skills_analysis['current_skills'])}")
            print(f"📚 Missing skills: {len(skills_analysis['missing_skills'])}")

            if skills_analysis["recommendations"]:
                print(
                    f"💡 Sample recommendations: {skills_analysis['recommendations'][:2]}"
                )

            return True
        else:
            print("❌ Resume not found for Career Bot test")
            return False

    except Exception as e:
        print(f"❌ Error testing Career Bot: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Starting AI Career Mentor Tests...\n")

    # Test 1: Resume parsing
    test1_passed = test_resume_parsing()

    # Test 2: Career bot
    test2_passed = test_career_bot()

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"📄 Resume Parser: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"🤖 Career Bot: {'✅ PASSED' if test2_passed else '❌ FAILED'}")

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Your chatbot is working correctly.")
        print("🚀 You can now proceed to use the Streamlit app.")
    else:
        print("\n⚠️ Some tests failed. Let's fix the issues first.")
        print("🔧 Check the error messages above for details.")


if __name__ == "__main__":
    main()
