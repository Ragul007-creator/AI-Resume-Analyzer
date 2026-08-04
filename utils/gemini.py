import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the resume against the job description.

Return ONLY valid JSON.

{{
    "ats_score": 0,
    "professional_summary": "",
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": []
}}

Job Description:
{job_description}

Resume:
{resume_text}
"""

    last_error = ""

    for _ in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            cleaned = response.text.strip()
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")
            cleaned = cleaned.strip()

            return json.loads(cleaned)

        except Exception as e:

            last_error = str(e)
            time.sleep(2)

    return {
        "ats_score": 0,
        "professional_summary": "Gemini failed.",
        "matching_skills": [],
        "missing_skills": [],
        "strengths": [],
        "weaknesses": [],
        "suggestions": [last_error]
    }


def extract_skills(text):

    prompt = f"""
Extract all technical skills from the text.

Return ONLY a JSON array.

Example:

[
    "Python",
    "FastAPI",
    "Docker",
    "AWS"
]

Text:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    cleaned = response.text.strip()
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    return json.loads(cleaned)