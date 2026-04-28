import pytesseract
from pdf2image import convert_from_path
from docx import Document

def procesar_pdf(input_pdf, output_word, pag_inicio=1, pag_fin=None):

    pages = convert_from_path(
        input_pdf,
        dpi=150,
        first_page=pag_inicio,
        last_page=pag_fin
    )

    texto_final = ""

    for page in pages:
        texto = pytesseract.image_to_string(page, lang='spa')
        texto_final += texto + "\n\n"

    doc = Document()
    for p in texto_final.split("\n"):
        if p.strip():
            doc.add_paragraph(p)

    doc.save(output_word)