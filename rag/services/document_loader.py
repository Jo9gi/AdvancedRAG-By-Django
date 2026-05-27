import os
# import fitz 
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOCUMENT_PATH = os.path.join(BASE_DIR,"documents","sample.txt")
DocPath = os.path.join(BASE_DIR,"documents","war_and_peace.pdf")

def load_document():
    with open(DOCUMENT_PATH,"r",encoding="utf-8") as file:
        text = file.read()
    return text

def DocPDF():
    doc = fitz.open(DocPath)

    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()

        full_text += text + "\n"

    return full_text
if __name__ == "__main__":
    data = load_document()
    # pdfData = DocPDF()
    print(data)
    # print(pdfData)

    