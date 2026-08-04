def calculate_ats_score(ai_result):

    score = ai_result.get("ats_score", 0)

    matched_skills = ai_result.get("matching_skills", [])

    missing_skills = ai_result.get("missing_skills", [])

    total = len(matched_skills) + len(missing_skills)

    if total == 0:
        skill_match = 0
    else:
        skill_match = int((len(matched_skills) / total) * 100)

    return (
        score,
        matched_skills,
        missing_skills,
        skill_match
    )