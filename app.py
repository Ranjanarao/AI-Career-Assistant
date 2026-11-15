import os
import requests
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

# ---------------- CONFIGURATION ----------------

load_dotenv()

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🎓",
    layout="wide"
)

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"

# ---------------- AI FUNCTION ----------------

def ask_ai(prompt):
    if not API_KEY:
        return "Gemini API key not found. Please check your .env file."

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1200
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return f"Gemini API Error ({response.status_code}): {response.text}"

        data = response.json()
        candidates = data.get("candidates", [])

        if not candidates:
            return "No answer received. Please try again."

        parts = candidates[0].get("content", {}).get("parts", [])
        answer = "\n".join(
            part.get("text", "")
            for part in parts
            if part.get("text")
        )

        return answer or "No text answer received."

    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"
    except (ValueError, KeyError, IndexError) as error:
        return f"Response error: {error}"


# ---------------- SESSION STATE ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- MAIN WEBSITE DESIGN ----------------

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #2563EB;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #64748b;
}
.module-card {
    padding: 20px;
    border-radius: 14px;
    background-color: rgba(128,128,128,0.10);
    border: 1px solid rgba(128,128,128,0.25);
    min-height: 150px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🎓 AI CAREER ASSISTANT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Smart Partner for Career Growth, Skills and Placement Preparation</div>',
    unsafe_allow_html=True
)

st.write("")
st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("🎯 Navigation")

module = st.sidebar.radio(
    "Choose Your Module",
    [
        "Home",
        "Career Chat",
        "Career Roadmap",
        "Placement Preparation",
        "Interview Generator",
        "Resume Analyzer"
    ]
)

st.sidebar.divider()
st.sidebar.info("AI-powered career guidance for students.")


# ---------------- HOME ----------------

if module == "Home":

    st.header("Welcome to Your AI Career Assistant 👋")
    st.write(
        "Explore career opportunities, improve your skills, "
        "prepare for interviews and build your professional future."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="module-card">
        <h3>💬 Career Chat</h3>
        <p>Ask questions about careers, technology and professional growth.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="module-card">
        <h3>📚 Career Roadmap</h3>
        <p>Get a personalized learning roadmap for your career goal.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="module-card">
        <h3>📄 Resume Analyzer</h3>
        <p>Upload your resume and receive improvement suggestions.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="module-card">
        <h3>🎯 Placement Preparation</h3>
        <p>Prepare for aptitude, technical skills and placement interviews.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="module-card">
        <h3>🎤 Interview Generator</h3>
        <p>Generate interview questions for your selected role.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.success("Select any module from the left sidebar to get started.")


# ---------------- CAREER CHAT ----------------

elif module == "Career Chat":

    st.header("💬 Career Chat")
    st.write("Ask anything about your career, skills, jobs or technology.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask your career-related question...")

    if question:
        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                answer = ask_ai(question)
            st.markdown(answer)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


# ---------------- CAREER ROADMAP ----------------

elif module == "Career Roadmap":

    st.header("📚 Career Roadmap Generator")

    goal = st.selectbox(
        "Select Your Career Goal",
        [
            "Software Developer",
            "AI / ML Engineer",
            "Cybersecurity Analyst",
            "Data Analyst",
            "Web Developer",
            "Cloud Engineer"
        ]
    )

    level = st.selectbox(
        "Select Your Current Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("Generate My Roadmap"):
        prompt = (
            f"Create a detailed practical career roadmap for a student "
            f"who wants to become a {goal}. Current level: {level}. "
            "Include skills, tools, projects, free learning resources "
            "and a realistic month-wise learning plan."
        )

        with st.spinner("Creating your roadmap..."):
            st.markdown(ask_ai(prompt))


# ---------------- PLACEMENT PREPARATION ----------------

elif module == "Placement Preparation":

    st.header("🎯 Placement Preparation")

    topic = st.selectbox(
        "Choose Your Preparation Topic",
        [
            "Aptitude",
            "Data Structures and Algorithms",
            "Python Programming",
            "DBMS",
            "Operating Systems",
            "Computer Networks",
            "HR Interview"
        ]
    )

    if st.button("Generate Preparation Plan"):
        prompt = (
            f"Create a beginner-friendly placement preparation plan "
            f"for {topic}. Include important concepts, daily practice "
            "tasks, examples and interview preparation tips."
        )

        with st.spinner("Preparing your plan..."):
            st.markdown(ask_ai(prompt))


# ---------------- INTERVIEW GENERATOR ----------------

elif module == "Interview Generator":

    st.header("🎤 Interview Question Generator")

    role = st.selectbox(
        "Select Job Role",
        [
            "Python Developer",
            "Cybersecurity Analyst",
            "AI / ML Engineer",
            "Web Developer",
            "Data Analyst",
            "Software Engineer"
        ]
    )

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("Generate Interview Questions"):
        prompt = (
            f"Generate 10 {difficulty} interview questions for "
            f"a {role} position. Give clear answers and simple "
            "explanations suitable for a student."
        )

        with st.spinner("Generating interview questions..."):
            st.markdown(ask_ai(prompt))


# ---------------- RESUME ANALYZER ----------------

elif module == "Resume Analyzer":

    st.header("📄 AI Resume Analyzer")
    st.write("Upload your resume in PDF format for feedback.")

    uploaded_file = st.file_uploader(
        "Upload Your Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:
            pdf = PdfReader(uploaded_file)
            resume_text = "\n".join(
                page.extract_text() or ""
                for page in pdf.pages
            )

            if not resume_text.strip():
                st.warning(
                    "No readable text found. Please upload a text-based PDF."
                )

            else:
                st.success("Resume uploaded successfully!")

                with st.expander("View Extracted Resume Text"):
                    st.text(resume_text[:5000])

                if st.button("Analyze My Resume"):
                    prompt = (
                        "Analyze this student's resume. Give feedback on "
                        "skills, projects, education, formatting, strengths "
                        "and improvements. Suggest practical changes.\n\n"
                        + resume_text[:12000]
                    )

                    with st.spinner("Analyzing your resume..."):
                        st.markdown(ask_ai(prompt))

        except Exception as error:
            st.error(f"Unable to read PDF: {error}")


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<center>🎓 AI Career Assistant | Built with Python, Streamlit and Gemini AI</center>",
    unsafe_allow_html=True
)