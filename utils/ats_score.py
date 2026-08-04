import re

TECH_SKILLS = [
    "python", "java", "c", "c++", "c#",
    "sql", "mysql", "postgresql", "mongodb",

    "html", "css", "javascript", "typescript",
    "react", "angular", "vue", "node.js",
    "express", "fastapi", "django", "flask",

    "streamlit", "rest api", "graphql",

    "git", "github", "docker", "kubernetes",
    "aws", "azure", "gcp", "linux",

    "numpy", "pandas", "matplotlib",
    "scikit-learn", "tensorflow", "pytorch",
    "machine learning", "deep learning",
    "nlp", "langchain", "prompt engineering",

    "power bi", "excel", "tableau",

    "ansys", "ansys fluent", "ansys workbench",
    "cfd", "computational fluid dynamics",
    "thermal engineering", "mechanical engineering",
    "electric vehicle", "product development"
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return text


def calculate_ats_score(resume_text, job_description):

    resume = clean_text(resume_text)
    job = clean_text(job_description)

    matched_skills = []
    missing_skills = []

    required_skills = []

    for skill in TECH_SKILLS:

        if skill in job:

            required_skills.append(skill)

            if skill in resume:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    matched_skills = sorted(set(matched_skills))
    missing_skills = sorted(set(missing_skills))

    if required_skills:
        skill_match = int(
            len(matched_skills) / len(required_skills) * 100
        )
    else:
        skill_match = 0

    score = 0

    breakdown = {}

    # ---------------- Skill Match (60 Marks) ----------------

    skill_score = int(skill_match * 0.6)
    score += skill_score
    breakdown["Skill Match"] = skill_score

    # ---------------- Education (10 Marks) ----------------

    education_score = 0

    if any(x in resume for x in [
        "b.e", "b.tech", "bachelor",
        "m.e", "m.tech", "master"
    ]):
        education_score = 10

    score += education_score
    breakdown["Education"] = education_score

    # ---------------- Projects (10 Marks) ----------------

    project_score = 0

    if "project" in resume:
        project_score = 10

    score += project_score
    breakdown["Projects"] = project_score

    # ---------------- Experience (10 Marks) ----------------

    experience_score = 0

    if any(x in resume for x in [
        "experience",
        "internship",
        "intern"
    ]):
        experience_score = 10

    score += experience_score
    breakdown["Experience"] = experience_score

    # ---------------- Certifications (10 Marks) ----------------

    certification_score = 0

    if any(x in resume for x in [
        "certificate",
        "certification",
        "certified"
    ]):
        certification_score = 10

    score += certification_score
    breakdown["Certifications"] = certification_score

    score = min(score, 100)

    return (
        score,
        matched_skills,
        missing_skills,
        skill_match,
        breakdown
    )