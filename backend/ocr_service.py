import numpy as np
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from docx import Document

def procesar_pdf(input_pdf, output_word, pag_inicio=1, pag_fin=None):
    ocr = PaddleOCR(use_angle_cls=True, lang='es')

    pages = convert_from_path(
        input_pdf,
        dpi=200,
        first_page=pag_inicio,
        last_page=pag_fin
    )

    texto_final = ""

    for page in pages:
        img = np.array(page)
        result = ocr.ocr(img, cls=True)

        if result and result[0]:
            for line in result[0]:
                texto_final += line[1][0] + "\n"

        texto_final += "\n\n"

    doc = Document()
    for p in texto_final.split("\n"):
        if p.strip():
            doc.add_paragraph(p)

    doc.save(output_word)