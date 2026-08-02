# '''import streamlit as st

# st.title("🤖 AI Resume Analyzer")

# st.write("Welcome to AI Resume Analyzer!")

# uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# job_description = st.text_area("Paste the Job Description")

# if st.button("Analyze Resume"):
#     st.success("Button Clicked!")'''
# '''import streamlit as st
# import fitz

# st.title("🤖 AI Resume Analyzer")

# uploaded_file = st.file_uploader(
#     "Upload your Resume (PDF)",
#     type=["pdf"]
# )

# job_description = st.text_area("Paste the Job Description")

# if uploaded_file is not None:

#     pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

#     resume_text = ""

#     for page in pdf:
#         resume_text += page.get_text()

#     pdf.close()

#     st.subheader("Extracted Resume Text")

#     st.text(resume_text[:1000])   # Shows first 1000 characters'''
#''' import streamlit as st
# import fitz

# st.title("🤖 AI Resume Analyzer")

# uploaded_file = st.file_uploader(
#     "Upload your Resume (PDF)",
#     type=["pdf"]
# )

# job_description = st.text_area("Paste the Job Description")

# if st.button("Analyze Resume"):

#     if uploaded_file is None:
#         st.warning("Please upload a resume.")
#     else:
#         pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

#         resume_text = ""

#         for page in pdf:
#             resume_text += page.get_text()

#         pdf.close()

#         st.subheader("Extracted Resume Text")
#         st.text(resume_text[:1000])   # First 1000 characters'''
#''' import streamlit as st
# from utils.pdf_reader import extract_text_from_pdf

# st.title("🤖 AI Resume Analyzer")

# uploaded_file = st.file_uploader(
#     "Upload your Resume (PDF)",
#     type=["pdf"]
# )

# job_description = st.text_area("Paste the Job Description")

# if st.button("Analyze Resume"):

#     if uploaded_file is None:
#         st.warning("Please upload a resume.")

#     else:
#         resume_text = extract_text_from_pdf(uploaded_file)

#         st.subheader("Extracted Resume Text")
#         st.text(resume_text[:1000])'''
import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.gemini import analyze_resume

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

✅ Skills Matching

✅ Resume Suggestions
""")

# ---------------- Main Page ----------------
st.title("🤖 AI Resume Analyzer")
st.caption("Upload your resume and compare it with any Job Description using Gemini AI.")

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

# Analyze Button
if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume.")
        st.stop()

    if job_description.strip() == "":
        st.warning("⚠️ Please paste the Job Description.")
        st.stop()

    # Extract Resume Text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Analyze with Gemini
    with st.spinner("🤖 AI is analyzing your resume..."):

        result = analyze_resume(
            resume_text,
            job_description
        )

    # Display Result
    st.success("✅ Analysis Completed")

    st.subheader("📄 AI Analysis")

    st.write(result)