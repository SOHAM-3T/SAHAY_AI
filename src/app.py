import streamlit as st
import os
from src.chatbot.career_bot import CareerBot
from src.utils.pdf_parser import extract_text_from_pdf
import tempfile

# Page config
st.set_page_config(page_title="AI-360 Career Mentor", page_icon="🤖", layout="wide")

# Custom CSS for better UI (simplified for compatibility)
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
</style>
""",
    unsafe_allow_html=True,
)


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
                career_bot = CareerBot(tmp_path)
                st.session_state["career_bot"] = career_bot
                st.session_state["resume_parsed"] = True

                # Show resume summary
                st.subheader("📋 Resume Summary")
                resume_data = career_bot.resume_data

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Skills", len(resume_data["skills"]))
                    st.metric("Projects", len(resume_data["projects"]))
                with col2:
                    st.metric("Experience", len(resume_data["experience"]))
                    st.metric("Education", len(resume_data["education"]))

                # Quick actions
                st.subheader("🚀 Quick Actions")
                if st.button("Analyze Skills Gap"):
                    st.session_state["show_skills_analysis"] = True

                if st.button("Career Path Suggestions"):
                    st.session_state["show_career_paths"] = True

            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
                st.exception(e)  # Show full error details

    # Main content area
    if "resume_parsed" in st.session_state:
        career_bot = st.session_state["career_bot"]

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
                            for skill in analysis["current_skills"][:10]:
                                st.write(f"• {skill}")

                        with col2:
                            st.subheader("📚 Skills to Develop")
                            for skill in analysis["missing_skills"][:10]:
                                st.write(f"• {skill}")

                        st.subheader("💡 Recommendations")
                        for rec in analysis["recommendations"]:
                            st.info(rec)
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


if __name__ == "__main__":
    main()
