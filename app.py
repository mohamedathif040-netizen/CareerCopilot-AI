import streamlit as st
from modules.resume_parser import extract_resume_text
from modules.gemini_analyzer import analyze_resume
import plotly.graph_objects as go
from modules.report_generator import generate_report
from modules.resume_pdf_generator import generate_resume_pdf

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "optimized_resume" not in st.session_state:
    st.session_state.optimized_resume = ""

st.set_page_config(
    page_title="CareerCopilot AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 35%,
        #312e81 70%,
        #4c1d95 100%
    );
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 18px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 10px 20px;
    margin-right: 8px;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    height: 3rem;
    font-weight: 600;
}

/* Download Buttons */
.stDownloadButton > button {
    border-radius: 12px;
    font-weight: 600;
}

/* Text Areas */
textarea {
    border-radius: 12px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
}

/* Hero Glow Effect */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    color: white;
    text-shadow: 0 0 20px rgba(99,102,241,0.6);
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    """
    <div class="main-title">
        🚀 CareerCopilot AI
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;color:#cbd5e1;'>From Resume to Interview</h4>",
    unsafe_allow_html=True
)

st.divider()

# Sidebar
with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.markdown("## CareerCopilot AI")

    st.success(
        "Your AI-powered career coach"
    )

    st.divider()

    st.markdown("""
### Features

✅ ATS Analysis

✅ Resume Optimization

✅ Career Roadmap

✅ Outreach Kit

✅ PDF Reports
""")

# Input Section
with st.container():
    st.subheader("📄 Resume Analysis")

    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "txt"]
        )

    with col2:
        recruiter_mode = st.selectbox(
            "Recruiter Persona",
            [
                "Silicon Valley Recruiter",
                "Google Recruiter",
                "Startup Founder",
                "HR Manager"
            ]
        )

    job_description = st.text_area(
        "Paste Job Description",
        height=200
    )

    analyze = st.button(
        "🚀 Analyze Resume",
        use_container_width=True
    )
if analyze:

    if resume_file is None:
        st.error("Please upload a resume")

    elif not job_description.strip():
        st.error("Please enter a job description")

    else:

        resume_text = extract_resume_text(
            resume_file
        )
        st.session_state.resume_text = resume_text
        with st.spinner(
            "Analyzing Resume..."
        ):
            result = analyze_resume(
               resume_text,
               job_description,
                recruiter_mode
            )
            st.session_state.analysis = result

        st.success("Resume Parsed Successfully")

        with st.expander("View Extracted Resume"):
            st.write(resume_text[:5000])

st.divider()

if st.session_state.analysis:

    result = st.session_state.analysis

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "ATS Score",
            result["ats_score"]
        )

    with col2:
        st.metric(
            "Keyword Match",
            f'{result["keyword_match"]}%'
        )

    with col3:
        st.metric(
            "Missing Skills",
            len(result["missing_skills"])
        )

    with col4:
        st.metric(
            "Interview Chance",
            f'{result["interview_probability"]}%'
        )
        
if st.session_state.analysis:

    result = st.session_state.analysis

    categories = [
        "ATS Score",
        "Keyword Match",
        "Interview Chance",
        "Resume Quality",
        "Project Strength"
    ]

    values = [
        result["ats_score"],
        result["keyword_match"],
        result["interview_probability"],
        min(result["ats_score"] + 10, 100),
        min(result["keyword_match"] + 15, 100)
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Profile Analysis"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
if st.session_state.analysis:

    result = st.session_state.analysis

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["ats_score"],
        title={"text": "🎯 Job Match Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"thickness": 0.4},
            "steps": [
                {"range": [0, 40], "color": "lightgray"},
                {"range": [40, 70], "color": "gray"},
                {"range": [70, 100], "color": "darkgray"}
            ]
        }
    ))

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
if st.session_state.analysis:

    result = st.session_state.analysis

    score = result["ats_score"]

    st.subheader("🚀 Application Readiness")

    st.progress(score / 100)

    if score >= 80:
        st.success(f"Excellent! Readiness Score: {score}%")

    elif score >= 60:
        st.warning(f"Good, but can improve. Score: {score}%")

    else:
        st.error(f"Needs significant improvement. Score: {score}%")

    
if st.session_state.analysis:

    result = st.session_state.analysis

    if st.button("📄 Generate PDF Report"):

        pdf_path = generate_report(
            result,
            "career_report.pdf"
        )

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="⬇ Download PDF",
                data=file,
                file_name="CareerCopilot_Report.pdf",
                mime="application/pdf"
            )
        
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
    "🔥 Recruiter Roast",
    "📈 Gap Analysis",
    "✍ Optimized Resume",
    "📩 Outreach Kit",
    "🗺 Career Roadmap"
    ]
)

with tab1:

    if st.session_state.analysis:

        result = st.session_state.analysis

        st.markdown(
            result["roast"]
        )
        
with tab2:

    if st.session_state.analysis:

        result = st.session_state.analysis

        st.subheader("Missing Skills")

        for skill in result["missing_skills"]:
            st.warning(skill)

        st.subheader("Improvement Plan")

        st.write(
            result["improvement_plan"]
        )
        
with tab3:

    if st.session_state.analysis:

        result = st.session_state.analysis

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("📄 Original Resume")

            st.text_area(
                "Original",
                st.session_state.resume_text,
                height=500
            )

        with col2:

            st.subheader("✨ Optimized Resume")

            st.text_area(
                "Optimized",
                result["optimized_resume"],
                height=500
            )

        pdf_path = generate_resume_pdf(
            result["optimized_resume"],
            "optimized_resume.pdf"
        )

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="📄 Download Professional Resume",
                data=pdf_file,
                file_name="CareerCopilot_Resume.pdf",
                mime="application/pdf"
            )
        
with tab4:

    if st.session_state.analysis:

        result = st.session_state.analysis

        st.subheader("🔗 LinkedIn Connection Request")

        st.text_area(
            "",
            result["linkedin_message"],
            height=120
        )

        st.subheader("📧 Cold Email")

        st.text_area(
            "",
            result["cold_email"],
            height=220
        )

        st.subheader("🤝 Referral Request")

        st.text_area(
            "",
            result["referral_request"],
            height=180
        )
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "📥 LinkedIn",
                result["linkedin_message"],
                file_name="linkedin_message.txt"
            )

        with col2:
            st.download_button(
                "📥 Cold Email",
                result["cold_email"],
                file_name="cold_email.txt"
            )

        with col3:
            st.download_button(
                "📥 Referral",
                result["referral_request"],
                file_name="referral_request.txt"
            )
            
with tab5:

    if st.session_state.analysis:

        result = st.session_state.analysis

        st.subheader(
            "🗺 Your Personalized Career Roadmap"
        )

        st.markdown(
            result["career_roadmap"]
        )