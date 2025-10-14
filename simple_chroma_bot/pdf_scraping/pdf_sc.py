import pdfplumber

path = "dummy_scrape_practice.pdf"   # PDF file ka path
output_file = "pdf_output.txt"       # Text file jisme save karna hai

with pdfplumber.open(path) as pdf, open(output_file, "w", encoding="utf-8") as file:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        file.write(f"\n--- PAGE {i} ---\n")   # Page header
        if text:
            file.write(text + "\n")          # Page ka text
        else:
            file.write("[No text found]\n")  # Agar page khali ho