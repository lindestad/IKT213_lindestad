from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

SOLUTIONS_PATH = Path(__file__).resolve().parent
PDF_PATH = SOLUTIONS_PATH / "assignment_4.pdf"


def main():
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    pdf.setTitle("Assignment 4 - Harris corners and image alignment")
    pdf.setAuthor("Daniel Lindestad")
    width, height = A4

    pages = [
        ("Harris corner detection", "harris.png", "Detected corners are marked in red."),
        ("Aligned image", "aligned.png", "Method: SIFT with FLANN and RANSAC."),
        (
            "Feature matches",
            "matches.png",
            "Green lines show the matches accepted by RANSAC.",
        ),
    ]
    for page_number, (title, filename, caption) in enumerate(pages, start=1):
        pdf.setFont("Helvetica", 10)
        pdf.drawString(36, height - 32, "IKT213 | Assignment 4 | Daniel Lindestad")
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(36, height - 60, title)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(36, height - 80, caption)

        image = ImageReader(str(SOLUTIONS_PATH / filename))
        image_width, image_height = image.getSize()
        scale = min((width - 72) / image_width, (height - 140) / image_height)
        image_width *= scale
        image_height *= scale
        pdf.drawImage(
            image,
            (width - image_width) / 2,
            40 + (height - 140 - image_height) / 2,
            width=image_width,
            height=image_height,
        )
        pdf.setFont("Helvetica", 9)
        pdf.drawRightString(width - 36, 22, f"{page_number} / 3")
        pdf.showPage()

    pdf.save()
    print(f"Written to {PDF_PATH}.")


if __name__ == "__main__":
    main()
