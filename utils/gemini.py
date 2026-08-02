import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(resume_text, job_description):

    prompt = f"""
    You are an expert ATS and HR recruiter.

    Analyze the following resume based on the given job description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Return your response in proper Markdown format.

# ATS Score
Score: XX/100

# Professional Summary
...

# Matching Skills
- Skill 1
- Skill 2
- Skill 3

# Missing Skills
- Skill 1
- Skill 2

# Strengths
- Point 1
- Point 2

# Weaknesses
- Point 1
- Point 2

# Suggestions
- Suggestion 1
- Suggestion 2
Only return the analysis. Do not include any introduction or conclusion."""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text