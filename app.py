import os
import fitz
from dotenv import load_dotenv
from google import genai

# Load API Key
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Open Resume PDF
pdf_path = "resume/Dharshan - Assosiate Software engineer.pdf"   # Change this to your PDF name

document = fitz.open(pdf_path)

resume_text = ""

for page in document:
    resume_text += page.get_text()

document.close()

# Prompt for Gemini
prompt = f"""
You are an expert HR recruiter.

Read the following resume and generate:

1. Professional Summary
2. Technical Skills
3. Strengths
4. Weaknesses
5. Top 5 suggestions to improve the resume

Resume:

{resume_text}
"""

# Send to Gemini
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)

print(response.text)