import pdfplumber
from PIL import Image
import pytesseract

path = "GSEB-Board-Class-9-Social-Science-Textbook-in-English.pdf"
output_file = "pdf_output_with_ocr.txt"

with pdfplumber.open(path) as pdf, open(output_file, "w", encoding="utf-8") as file:
    for i, page in enumerate(pdf.pages, start=1):
        file.write(f"\n--- PAGE {i} ---\n")

        # Pehle try karo normal text extract karne ka
        text = page.extract_text()
        if text:
            file.write(text + "\n")
        else:
            # Agar text nahi mila toh image OCR se karo
            im = page.to_image(resolution=300).original  # page ko image banao
            text = pytesseract.image_to_string(im, lang="eng")
            file.write(text + "\n")
