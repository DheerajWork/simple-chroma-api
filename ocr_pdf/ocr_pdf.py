import pytesseract
from pdf2image import convert_from_path
from PIL import Image

pdf_path = "exam paper.pdf"   
output_file = "ocr_output.txt"


pages = convert_from_path(pdf_path)

with open(output_file, "w", encoding="utf-8") as f:
    for i, page in enumerate(pages, start=1):
        
        text = pytesseract.image_to_string(page, lang="eng")  
        
        f.write(f"\n--- PAGE {i} ---\n")
        if text.strip():
            f.write(text + "\n")
        else:
            f.write("[No text found]\n")

            
