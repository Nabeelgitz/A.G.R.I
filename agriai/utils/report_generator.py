from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import enums
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


def create_pdf_report(report, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm
    )

    styles = getSampleStyleSheet()

    title_style = styles['Title']
    heading_style = styles['Heading2']
    body_style = styles['BodyText']

    title_style.textColor = colors.darkgreen
    heading_style.textColor = colors.HexColor("#1B4332")

    body_style.leading = 20
    body_style.spaceAfter = 10
    body_style.fontSize = 11

    elements = []

    # Title
    elements.append(
        Paragraph(
            "AGRICULTURAL AI REPORT",
            title_style
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    lines = report.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            elements.append(Spacer(1, 6))
            continue

        # Heading detection
        if (
            line[0].isdigit()
            and "." in line[:5]
        ):
            elements.append(
                Paragraph(
                    line,
                    heading_style
                )
            )

        # Bullet point
        elif line.startswith("-"):
            elements.append(
                Paragraph(
                    f"• {line[1:].strip()}",
                    body_style
                )
            )

        # Normal paragraph
        else:
            elements.append(
                Paragraph(
                    line,
                    body_style
                )
            )

    doc.build(elements)

    return filename