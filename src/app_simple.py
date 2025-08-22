import streamlit as st
import os
import sys
import tempfile

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Import our working modules
from utils.pdf_parser import extract_text_from_pdf
from utils.resume_parser import parse_resume

# Page config
st.set_page_config(page_title="AI-360 Career Mentor", page_icon="🤖", layout="wide")

# Custom CSS for better UI
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


def create_simple_career_bot(resume_data):
    """Create a simple career bot without RAG dependencies"""

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
                "ml engineer": [
                    "Python",
                    "Machine Learning",
                    "Deep Learning",
                    "MLOps",
                    "Data Engineering",
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
                elif "statistics" in skill.lower():
                    recommendations.append(
                        f"Learn {skill}: Take Statistics courses on Khan Academy or edX"
                    )
                elif "data visualization" in skill.lower():
                    recommendations.append(
                        f"Learn {skill}: Master Tableau, Power BI, or Python libraries like Matplotlib"
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
            if any("java" in skill.lower() for skill in skills):
                career_paths.append("Java Developer")
                career_paths.append("Android Developer")

            return career_paths or ["General Software Developer", "IT Consultant"]

        def get_career_advice(self, question: str) -> str:
            """Provide career advice based on the question"""
            question_lower = question.lower()

            if "skill" in question_lower and "gap" in question_lower:
                return "I can help you analyze skills gaps! Use the 'Analyze Skills Gap' feature above to see what skills you need for your target role."

            elif "career" in question_lower and "path" in question_lower:
                return "Great question! Click on 'Career Path Suggestions' to see what career paths align with your current skills and background."

            elif "resume" in question_lower:
                return f"Your resume shows {len(self.resume_data['skills'])} skills, {len(self.resume_data['projects'])} projects, and {len(self.resume_data['education'])} education items. You're well-positioned for tech roles!"

            elif "python" in question_lower:
                if any(
                    "python" in skill.lower() for skill in self.resume_data["skills"]
                ):
                    return "Great! You already have Python skills. Consider building more projects and learning advanced topics like Django, Flask, or data science libraries."
                else:
                    return "Python is a great skill to add! Start with basic syntax, then move to web development or data science depending on your interests."

            else:
                return "I'm here to help with your career! You can ask me about skills, career paths, resume improvement, or use the interactive features above."

    return SimpleCareerBot(resume_data)


def main():
    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>🤖 AI-360 Career Mentor</h1>
        <p>Your AI-powered career advisor that analyzes resumes and provides personalized guidance</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar for resume upload
    with st.sidebar:
        st.header("📄 Resume Upload")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"],
            help="Upload your resume to get personalized career advice",
        )

        if uploaded_file is not None:
            st.success("✅ Resume uploaded successfully!")

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            # Initialize career bot
            try:
                # Parse resume
                raw_text = extract_text_from_pdf(tmp_path)
                parsed_data = parse_resume(raw_text)

                # Create career bot
                career_bot = create_simple_career_bot(parsed_data)

                # Store in session state
                st.session_state["career_bot"] = career_bot
                st.session_state["resume_data"] = parsed_data
                st.session_state["resume_parsed"] = True

                # Show resume summary
                st.subheader("📋 Resume Summary")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Skills", len(parsed_data["skills"]))
                    st.metric("Projects", len(parsed_data["projects"]))
                with col2:
                    st.metric("Experience", len(parsed_data["experience"]))
                    st.metric("Education", len(parsed_data["education"]))

                # Show sample skills
                if parsed_data["skills"]:
                    st.write("🛠️ **Sample Skills:**")
                    st.write(", ".join(parsed_data["skills"][:10]))

                # Quick actions
                st.subheader("🚀 Quick Actions")
                if st.button("Analyze Skills Gap"):
                    st.session_state["show_skills_analysis"] = True

                if st.button("Career Path Suggestions"):
                    st.session_state["show_career_paths"] = True

            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
                st.exception(e)

    # Main content area
    if "resume_parsed" in st.session_state:
        career_bot = st.session_state["career_bot"]
        resume_data = st.session_state["resume_data"]

        # Skills Gap Analysis
        if st.session_state.get("show_skills_analysis", False):
            st.header("🔍 Skills Gap Analysis")

            target_role = st.selectbox(
                "Select your target role:",
                [
                    "Data Scientist",
                    "Software Engineer",
                    "Product Manager",
                    "Data Analyst",
                    "ML Engineer",
                ],
            )

            if st.button("Analyze"):
                with st.spinner("Analyzing your skills..."):
                    try:
                        analysis = career_bot.suggest_skills(target_role)

                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("✅ Your Current Skills")
                            st.write(
                                f"**Total Skills:** {len(analysis['current_skills'])}"
                            )
                            if analysis["current_skills"]:
                                for skill in analysis["current_skills"][:10]:
                                    st.write(f"• {skill}")

                        with col2:
                            st.subheader("📚 Skills to Develop")
                            st.write(
                                f"**Missing Skills:** {len(analysis['missing_skills'])}"
                            )
                            if analysis["missing_skills"]:
                                for skill in analysis["missing_skills"]:
                                    st.write(f"• {skill}")

                        if analysis["recommendations"]:
                            st.subheader("💡 Learning Recommendations")
                            for rec in analysis["recommendations"]:
                                st.info(rec)

                        # Show progress
                        current_count = len(analysis["current_skills"])
                        missing_count = len(analysis["missing_skills"])
                        total_required = current_count + missing_count
                        progress = (
                            current_count / total_required if total_required > 0 else 0
                        )

                        st.subheader("📊 Skills Progress")
                        st.progress(progress)
                        st.write(
                            f"You have **{current_count}** out of **{total_required}** required skills ({progress:.1%})"
                        )

                    except Exception as e:
                        st.error(f"Error analyzing skills: {str(e)}")
                        st.exception(e)

        # Career Path Suggestions
        if st.session_state.get("show_career_paths", False):
            st.header("🛤️ Career Path Suggestions")

            with st.spinner("Analyzing your profile..."):
                try:
                    career_paths = career_bot.get_career_path_suggestions()

                    st.subheader("Based on your skills, consider these career paths:")
                    for i, path in enumerate(career_paths, 1):
                        st.write(f"{i}. **{path}**")

                    # Show skill alignment
                    if career_paths:
                        st.subheader("🎯 Why These Paths Fit You")
                        skills = set(resume_data["skills"])

                        if any("python" in skill.lower() for skill in skills):
                            st.write(
                                "✅ **Python Skills**: Great for Data Science, Software Engineering, and ML"
                            )
                        if any("java" in skill.lower() for skill in skills):
                            st.write(
                                "✅ **Java Skills**: Perfect for Enterprise Software and Android Development"
                            )
                        if any("sql" in skill.lower() for skill in skills):
                            st.write(
                                "✅ **SQL Skills**: Essential for Data Analysis and Business Intelligence"
                            )
                        if any("machine learning" in skill.lower() for skill in skills):
                            st.write(
                                "✅ **ML Skills**: Excellent for AI/ML Engineering and Research"
                            )

                except Exception as e:
                    st.error(f"Error getting career paths: {str(e)}")
                    st.exception(e)

        # Chat Interface
        st.header("💬 Ask Career Questions")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about your career, skills, or job search..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = career_bot.get_career_advice(prompt)
                        st.markdown(response)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_msg}
                        )

    else:
        # Welcome message
        st.info("📄 Please upload your resume in the sidebar to get started!")

        # Demo features
        st.header("🎯 What This Bot Can Do")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
            **📋 Resume Analysis**
            - Extract skills, experience, education
            - Identify key strengths
            - Parse project details
            """
            )

        with col2:
            st.markdown(
                """
            **🔍 Skills Gap Analysis**
            - Compare your skills with target roles
            - Identify missing competencies
            - Provide learning recommendations
            """
            )

        with col3:
            st.markdown(
                """
            **💡 Career Guidance**
            - Personalized career advice
            - Job search strategies
            - Interview preparation tips
            """
            )

        # Show sample resume data
        st.header("📊 Sample Resume Analysis")
        st.write("Here's what your resume analysis will look like:")

        sample_data = {"Skills": 47, "Projects": 16, "Education": 5, "Experience": 0}

        cols = st.columns(4)
        for i, (key, value) in enumerate(sample_data.items()):
            with cols[i]:
                st.metric(key, value)


if __name__ == "__main__":
    main()
