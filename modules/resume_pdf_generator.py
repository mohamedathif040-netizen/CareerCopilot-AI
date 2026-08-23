from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_resume_pdf(resume_text, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Optimized Resume",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    for line in resume_text.split("\n"):
        if line.strip():
            content.append(
                Paragraph(
                    line,
                    styles["Normal"]
                )
            )

    doc.build(content)

    return filename