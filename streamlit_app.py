import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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

st.caption(
    "Upload your resume and compare it with any Job Description using Gemini AI."
)

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

if st.button("🚀 Analyze Resume", width="stretch"):

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
    score, matched_skills, missing_skills, skill_match, breakdown = calculate_ats_score(
        resume_text,
        job_description
    )
    # DEBUG (Remove after testing)
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
        st.markdown("### 📈 ATS Gauge")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "ATS Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2563EB"},
                    "steps": [
                        {"range": [0, 40], "color": "#FCA5A5"},
                        {"range": [40, 60], "color": "#FCD34D"},
                        {"range": [60, 80], "color": "#86EFAC"},
                        {"range": [80, 100], "color": "#22C55E"},
                    ],
                },
            )
        )

        gauge.update_layout(height=350)

        st.plotly_chart(gauge, width="stretch")

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
            width="stretch"
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
        st.markdown("### 📊 Skills Comparison")

        bar_fig = px.bar(
            x=["Matched Skills", "Missing Skills"],
            y=[len(matched_skills), len(missing_skills)],
            color=["Matched Skills", "Missing Skills"],
            color_discrete_map={
                "Matched Skills": "#22C55E",
                "Missing Skills": "#EF4444"
            },
            labels={"x": "Category", "y": "Count"},
            title="Matched vs Missing Skills"
        )

        st.plotly_chart(
            bar_fig,
            width="stretch"
        )

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
    # ==================================================
    # Learning Roadmap
    # ==================================================

    ROADMAP = {
        "python": [
            "Learn Python fundamentals",
            "Practice OOP",
            "Solve coding problems"
        ],
        "docker": [
            "Learn Docker basics",
            "Understand Dockerfiles",
            "Practice Docker Compose"
        ],
        "aws": [
            "Learn EC2",
            "Learn S3",
            "Understand IAM"
        ],
        "fastapi": [
            "Build REST APIs",
            "Use Pydantic",
            "Deploy FastAPI applications"
        ],
        "django": [
            "Learn Models",
            "Learn Views",
            "Build CRUD applications"
        ],
        "react": [
            "Learn Components",
            "Understand Hooks",
            "Build Projects"
        ],
        "langchain": [
            "Prompt Templates",
            "Chains",
            "RAG Applications"
        ],
        "prompt engineering": [
            "Prompt Design",
            "Few-shot Prompting",
            "System Prompts"
        ],
        "machine learning": [
            "Supervised Learning",
            "Model Evaluation",
            "Scikit-learn"
        ]
    }

    st.markdown("## 🚀 Learning Roadmap")

    roadmap_col1, roadmap_col2 = st.columns(2)

    if missing_skills:

        for i, skill in enumerate(missing_skills):

            column = roadmap_col1 if i % 2 == 0 else roadmap_col2

            with column:

                st.markdown(f"### 📘 {skill.title()}")

                if skill in ROADMAP:

                    for topic in ROADMAP[skill]:
                        st.write(f"• {topic}")

                else:
                    st.write("• Learn the fundamentals")
                    st.write("• Practice with projects")
                    st.write("• Build portfolio projects")

    else:
        st.success("🎉 Your resume already matches all detected skills!")   
    st.success("✅ Analysis Completed")
    st.balloons()
    # ==================================================
    # ATS Score Breakdown
    # ==================================================

    st.markdown("## 📊 ATS Score Breakdown")

    for category, marks in breakdown.items():

        if category == "Skill Match":
            max_marks = 60
        else:
            max_marks = 10

        st.metric(
            label=category,
            value=f"{marks}/{max_marks}"
        )
    # ==================================================
    # Resume Checklist
    # ==================================================

    st.markdown("## ✅ Resume Checklist")

    check1, check2 = st.columns(2)

    resume_lower = resume_text.lower()

    checks = {
        "Contact Information": any(x in resume_lower for x in ["@", "phone", "mobile", "+91"]),
        "Education": any(x in resume_lower for x in ["education", "b.e", "b.tech", "bachelor", "master"]),
        "Projects": "project" in resume_lower,
        "Experience": any(x in resume_lower for x in ["experience", "internship", "intern"]),
        "Skills": "skills" in resume_lower,
        "Certifications": any(x in resume_lower for x in ["certification", "certificate", "certified"]),
        "GitHub": "github" in resume_lower,
        "LinkedIn": "linkedin" in resume_lower,
    }

    items = list(checks.items())
    checklist_score = sum(checks.values())
    checklist_percentage = int((checklist_score / len(checks)) * 100)
    st.metric(
        "📋 Checklist Score",
        f"{checklist_score}/{len(checks)}",
        f"{checklist_percentage}%"
    )

    st.progress(checklist_percentage / 100)
    # ==================================================
    # Job Readiness
    # ==================================================

    readiness = int(
        (score * 0.5) +
        (skill_match * 0.3) +
        (checklist_percentage * 0.2)
    )

    st.markdown("## 🚀 Job Readiness")

    st.progress(readiness / 100)

    if readiness >= 85:
        st.success(f"🎯 {readiness}% - Ready to Apply")

    elif readiness >= 70:
        st.info(f"👍 {readiness}% - Almost Ready")

    elif readiness >= 50:
        st.warning(f"⚡ {readiness}% - Needs Improvement")

    else:
        st.error(f"📚 {readiness}% - More Preparation Needed")
    # ==================================================
        # Recruiter Tips
        # ==================================================
    
    st.markdown("## 💼 Recruiter Tips")
    
    tips = []
    
    if score < 60:
        tips.append("Tailor your resume for every job application.")
        tips.append("Include more job-relevant technical skills.")
        tips.append("Improve your ATS score by adding measurable achievements.")
    
    if skill_match < 70:
        tips.append("Learn the missing technical skills before applying.")
        tips.append("Highlight the skills you already possess more clearly.")
    
    if checklist_percentage < 100:
        tips.append("Complete all important resume sections such as GitHub, LinkedIn, Certifications, and Projects.")
    
    if score >= 80:
        tips.append("Your resume is strong. Focus on interview preparation.")
    
    for tip in tips:
        st.info(f"💡 {tip}")
    with check1:
        for title, status in items[:4]:
            if status:
                st.success(f"✅ {title}")
            else:
                st.error(f"❌ {title}")

    with check2:
        for title, status in items[4:]:
            if status:
                st.success(f"✅ {title}")
            else:
                st.error(f"❌ {title}")

    # ==================================================
    # AI REPORT
    # ==================================================

    st.subheader("📄 AI Analysis Report")

    st.markdown("### 👤 Professional Summary")
    st.info(result["professional_summary"])

    st.markdown("### ✅ Matching Skills")

    if result["matching_skills"]:
        for skill in result["matching_skills"]:
            st.success(skill)
    else:   
        st.info("AI analysis unavailable.")

    st.markdown("### ❌ Missing Skills")

    if result["missing_skills"]:
        for skill in result["missing_skills"]:
            st.error(skill)
    else:
        st.info("AI analysis unavailable.")

    st.markdown("### 💪 Strengths")

    if result["strengths"]:
        for strength in result["strengths"]:
            st.success(strength)
    else:
        st.info("AI analysis unavailable.")

    st.markdown("### ⚠️ Weaknesses")

    if result["weaknesses"]:
        for weakness in result["weaknesses"]:
            st.warning(weakness)
    else:
        st.info("AI analysis unavailable.")

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
            width="stretch"
        )

# ======================================================
# Footer
# ======================================================

st.markdown("---")

st.caption("🚀 Built with ❤️ using Streamlit + Google Gemini AI")
st.caption("👨‍💻 Developed by Ragul M")