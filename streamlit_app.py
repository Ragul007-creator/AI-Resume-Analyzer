import streamlit as st
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer

from utils.pdf_reader import extract_text_from_pdf
from utils.gemini import analyze_resume
from utils.ats_score import calculate_ats_score
from utils.pdf_generator import generate_pdf

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Sidebar ----------------
st.sidebar.title("🤖 AI Resume Analyzer")

st.sidebar.markdown("""
### Features

✅ Resume Analysis

✅ ATS Score

✅ Skill Match

✅ Resume Suggestions

✅ PDF Report
""")

# ---------------- Main Page ----------------
st.title("🤖 AI Resume Analyzer")
st.caption("Upload your resume and compare it with any Job Description using Gemini AI.")

st.info(
    "📌 Upload your resume, paste the Job Description, and click **🚀 Analyze Resume**."
)

st.markdown("---")

# Top Cards
top1, top2 = st.columns(2)

with top1:
    st.info("📄 Supported Format: PDF")

with top2:
    st.info("🤖 AI Model: Gemini")

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

# Job Description
job_description = st.text_area(
    "Paste the Job Description",
    height=200
)

# ======================================================
# Analyze Button
# ======================================================

if st.button("🚀 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume.")
        st.stop()

    if job_description.strip() == "":
        st.warning("⚠️ Please paste the Job Description.")
        st.stop()

    # Extract Resume Text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Resume Preview
    st.subheader("📄 Resume Preview")

    pdf_viewer(
        uploaded_file.getvalue(),
        width=700,
        height=800
    )

    st.markdown("---")

    # Gemini Analysis
    with st.spinner("🤖 AI is analyzing your resume..."):
        result = analyze_resume(
            resume_text,
            job_description
        )

    # ATS Score
    score, matched_skills, missing_skills, skill_match = calculate_ats_score(
        result
    )
    st.write("DEBUG")
    st.write("Matched:", matched_skills)
    st.write("Missing:", missing_skills)
    st.write("Score:", score)
    st.write("Skill Match:", skill_match)

    # ==================================================
    # Dashboard
    # ==================================================

    st.subheader("📊 Resume Dashboard")

    card1, card2, card3 = st.columns(3)

    with card1:
        st.markdown(f"""
        <div style="background:#1E3A8A;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:white;">
            <h4>📊 ATS Score</h4>
            <h1>{score}/100</h1>
        </div>
        """, unsafe_allow_html=True)

    with card2:
        st.markdown(f"""
        <div style="background:#047857;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:white;">
            <h4>🎯 Skill Match</h4>
            <h1>{skill_match}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📈 ATS Progress")

    st.progress(score / 100)

    st.write(f"**Overall ATS Score:** {score}/100")
    if score >= 90:
        st.success("🏆 Outstanding! Your resume is highly optimized for this job.")

    elif score >= 75:
        st.success("✅ Strong Match! Your resume matches the job requirements well.")

    elif score >= 60:
        st.warning("🟡 Good Match. Improve a few skills to increase your chances.")

    elif score >= 40:
        st.warning("🟠 Average Match. Your resume needs more relevant skills.")

    else:
        st.error("🔴 Poor Match. Consider tailoring your resume before applying.")

    with card3:

        if score >= 80:
            fit = "🟢 Excellent"
            color = "#16A34A"

        elif score >= 60:
            fit = "🟡 Good"
            color = "#F59E0B"

        elif score >= 40:
            fit = "🟠 Average"
            color = "#EA580C"

        else:
            fit = "🔴 Poor"
            color = "#DC2626"

        st.markdown(
            f"""
            <div style="
                background:{color};
                padding:20px;
                border-radius:15px;
                text-align:center;
                color:white;
            ">
                <h4>🎯 Job Fit</h4>
                <h1>{fit}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==================================================
    # Pie Chart
    # ==================================================

    chart1, chart2 = st.columns(2)

    with chart1:

        fig = px.pie(
        names=["Matched Skills", "Missing Skills"],
        values=[
            len(matched_skills),
            len(missing_skills)
        ],
        hole=0.55,
        title="📊 Skill Distribution",
        color=["Matched Skills", "Missing Skills"],
        color_discrete_map={
            "Matched Skills": "#22C55E",
            "Missing Skills": "#EF4444"
        }
    )
        fig.update_traces(
            textinfo="percent+label",
            textfont_size=14,
            pull=[0.03, 0]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.markdown("### 📌 Resume Statistics")

        stat1, stat2, stat3 = st.columns(3)

        with stat1:
            st.metric(
                "Matched Skills",
                len(matched_skills)
            )

        with stat2:
            st.metric(
                "Missing Skills",
                len(missing_skills)
            )

        with stat3:
            st.metric(
                "Job Skills",
                len(matched_skills) + len(missing_skills)
            )

    with chart2:

        if score >= 80:
            st.success("🟢 Excellent ATS Score!")

        elif score >= 60:
            st.warning("🟡 Good ATS Score!")

        else:
            st.error("🔴 Low ATS Score!")

    # ==================================================
    # Skills
    # ==================================================

    skill1, skill2 = st.columns(2)

    with skill1:

        st.subheader("✅ Matched Skills")

        if matched_skills:

            for skill in matched_skills:
                st.success(skill.title())

        else:
            st.info("No matching skills found.")

    with skill2:

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:
                st.error(skill.title())

        else:
            st.success("🎉 No missing skills!")

    st.success("✅ Analysis Completed")
    st.balloons()

    # ==================================================
    # AI REPORT
    # ==================================================

    st.subheader("📄 AI Analysis Report")

    st.markdown("### 👤 Professional Summary")
    st.info(result["professional_summary"])

    st.markdown("### ✅ Matching Skills")

    for skill in result["matching_skills"]:
        st.success(skill)

    st.markdown("### ❌ Missing Skills")

    for skill in result["missing_skills"]:
        st.error(skill)

    st.markdown("### 💪 Strengths")

    for strength in result["strengths"]:
        st.success(strength)

    st.markdown("### ⚠️ Weaknesses")

    for weakness in result["weaknesses"]:
        st.warning(weakness)

    st.markdown("### 💡 Suggestions")

    for suggestion in result["suggestions"]:
        st.info(suggestion)

    # ==================================================
    # PDF
    # ==================================================

    pdf_file = generate_pdf(
        result,
        score,
        skill_match
    )

    with open(pdf_file, "rb") as pdf:

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name="Resume_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# ======================================================
# Footer
# ======================================================

st.markdown("---")

st.caption("🚀 Built with ❤️ using Streamlit + Google Gemini AI")
st.caption("👨‍💻 Developed by Ragul M")