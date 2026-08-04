from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from datetime import datetime

styles = getSampleStyleSheet()

title_style = styles["Title"]
title_style.alignment = TA_CENTER
title_style.textColor = HexColor("#1E3A8A")

heading_style = styles["Heading2"]
heading_style.textColor = HexColor("#1565C0")

normal_style = styles["BodyText"]


def generate_pdf(result, score, skill_match):

    filename = "Resume_Analysis_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    # ===========================
    # Title
    # ===========================

    story.append(
        Paragraph(
            "<font size=22><b>AI Resume Analysis Report</b></font>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "<font color='#666666'>Professional ATS Analysis Report</font>",
            normal_style
        )
    )

    story.append(Spacer(1, 0.35 * inch))

    # ===========================
    # Job Fit
    # ===========================

    if score >= 80:
        job_fit = "Excellent"

    elif score >= 60:
        job_fit = "Good"

    elif score >= 40:
        job_fit = "Average"

    else:
        job_fit = "Poor"

    # ===========================
    # Summary Table
    # ===========================
    story.append(
    Paragraph(
        "<font size=16 color='#1565C0'><b>Resume Summary</b></font>",
        heading_style
        )
    )

    story.append(Spacer(1, 10))

    table_data = [
        ["ATS Score", f"{score}/100"],
        ["Skill Match", f"{skill_match}%"],
        ["Job Fit", job_fit],
        ["Generated On", datetime.now().strftime("%d-%m-%Y %H:%M")]
    ]

    table = Table(table_data, colWidths=[2.5 * inch, 3 * inch])

    table.setStyle(TableStyle([

    ("BACKGROUND", (0, 0), (0, -1), HexColor("#1565C0")),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

    ("BACKGROUND", (1, 0), (1, -1), HexColor("#F8FAFC")),

    ("GRID", (0, 0), (-1, -1), 0.75, HexColor("#D1D5DB")),

    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

    ("FONTSIZE", (0, 0), (-1, -1), 11),

    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 12),

    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

]))

    story.append(table)

    story.append(Spacer(1, 20))

    # ===========================
    # Professional Summary
    # ===========================

    story.append(
        Paragraph(
            "Professional Summary",
            heading_style
        )
    )

    story.append(
        Paragraph(
            result["professional_summary"],
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # ===========================
    # Helper Function
    # ===========================

    def add_section(title, items):

        story.append(
            Paragraph(
                "<font color='#1565C0'><b>" + title + "</b></font>",
                heading_style
            )
        )

        story.append(Spacer(1, 5))

        if items:

            for item in items:

                story.append(
                    Paragraph(
                        f"✔ {item}",
                        normal_style
                    )
                )

        else:

            story.append(
                Paragraph(
                    "<font color='grey'>No information available.</font>",
                    normal_style
                )
            )

        story.append(Spacer(1, 8))

        story.append(
            Paragraph(
                "<font color='#D1D5DB'>____________________________________________________________</font>",
                normal_style
            )
        )

        story.append(Spacer(1, 12))

    # ===========================
    # Sections
    # ===========================

    add_section("Matching Skills", result["matching_skills"])
    add_section("Missing Skills", result["missing_skills"])
    add_section("Strengths", result["strengths"])
    add_section("Weaknesses", result["weaknesses"])
    add_section("Suggestions", result["suggestions"])

    # ===========================
    # Footer
    # ===========================

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "<font color='#D1D5DB'>____________________________________________________________</font>",
            normal_style
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>AI Resume Analyzer Report</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Generated using Google Gemini AI and Streamlit",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"Report Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "<b>Developed by Ragul M</b>",
            normal_style
        )
    )

    doc.build(story)

    return filename