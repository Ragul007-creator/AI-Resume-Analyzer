import re


def format_analysis(result):

    sections = [
        "Professional Summary",
        "Matching Skills",
        "Missing Skills",
        "Strengths",
        "Weaknesses",
        "Suggestions"
    ]

    formatted = {}

    for i, section in enumerate(sections):

        if i < len(sections) - 1:
            pattern = rf"# {section}(.*?)# {sections[i+1]}"
        else:
            pattern = rf"# {section}(.*)"

        match = re.search(
            pattern,
            result,
            re.S
        )

        if match:
            formatted[section] = match.group(1).strip()
        else:
            formatted[section] = "Not Available"

    return formatted