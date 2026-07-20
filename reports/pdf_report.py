from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

import os


def generate_pdf(results):

    os.makedirs("exports", exist_ok=True)

    pdf_path = "exports/recruiter_report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>AI Resume Screening Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1,20))

    for i, candidate in enumerate(results,start=1):

        story.append(
            Paragraph(
                f"<b>Rank {i}</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"Candidate : {candidate['candidate']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Final Score : {candidate['final_score']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Semantic Score : {candidate['semantic_score']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Skill Score : {candidate['skill_score']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Recommendation : {candidate['recommendation']}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,18))

    doc.build(story)

    return pdf_path