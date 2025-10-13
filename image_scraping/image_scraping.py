from PIL import Image
import pytesseract

image_file = "test.png"
output_file = "output.txt"

img = Image.open(image_file)


text = pytesseract.image_to_string(img, lang="eng")


with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)
