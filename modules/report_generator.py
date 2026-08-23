from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(result, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "CareerCopilot AI Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"ATS Score: {result['ats_score']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Keyword Match: {result['keyword_match']}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Interview Chance: {result['interview_probability']}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Recruiter Roast",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            result["roast"],
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Career Roadmap",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            result["career_roadmap"],
            styles["Normal"]
        )
    )

    doc.build(content)

    return filename