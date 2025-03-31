from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
import re

def save_summary_as_pdf(summary, title):
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    pdf_filename = f"{safe_title}.pdf"

    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    textobject = c.beginText(40, height - 50)
    textobject.setFont("Helvetica", 12)

    for paragraph in summary.split("\n"):
        wrapped = wrap(paragraph, width=90)
        for line in wrapped:
            textobject.textLine(line)
        textobject.textLine("")

    c.drawText(textobject)
    c.save()

    print(f"📄 PDF gerado: {pdf_filename}")
