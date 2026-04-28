import os
import time
import numpy as np
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from docx import Document
from groq import Groq

def corregir_texto_con_ia(texto_bruto, api_key):
    if len(texto_bruto.strip()) < 10:
        return texto_bruto

    client = Groq(api_key=api_key)
    
    prompt = f"""
    Eres un editor experto. Tu tarea es corregir la ortografía, gramática, puntuación y uso de mayúsculas 
    del siguiente texto extraído de un PDF mediante OCR. 
    Reglas:
    - Mantén la estructura original de los párrafos y los saltos de línea.
    - No cambies el significado ni agregues información nueva.
    - Si identificas caracteres raros o extraños como ä en lugar de á, ô en lugar de ó, etc, corrígelos.
    - Une las palabras que estén partidas por el salto de línea u oraciones.
    - Devuelve ÚNICAMENTE el texto corregido, sin saludos ni comentarios adicionales.
    
    Texto a corregir:
    {texto_bruto}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", 
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"[!] Error con Groq en esta página: {e}")
        return texto_bruto

def procesar_pdf(input_pdf, output_word, pag_inicio=1, pag_fin=None):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("La API Key de Groq no está configurada en las variables de entorno.")

    ocr = PaddleOCR(use_angle_cls=True, lang='es')
    
    pages = convert_from_path(
        input_pdf,
        dpi=150, # Reducido a 150 para que no consuma tanta memoria RAM en Render
        first_page=pag_inicio,
        last_page=pag_fin
    )

    texto_final = ""

    for i, page in enumerate(pages):
        img = np.array(page)
        h, w, _ = img.shape
        
        # Eliminar márgenes superior e inferior
        top_crop = int(h * 0.12)    
        bottom_crop = int(h * 0.87)  
        img_cropped = img[top_crop:bottom_crop, :]

        result = ocr.ocr(img_cropped)
        texto_pagina_bruto = ""

        if result and result[0]:
            lineas = []
            for line in result[0]:
                text = line[1][0]
                box = line[0]
                y = box[0][1]
                lineas.append((y, text))

            lineas.sort(key=lambda x: x[0])
            for _, texto in lineas:
                texto_pagina_bruto += texto + "\n"

        texto_corregido = corregir_texto_con_ia(texto_pagina_bruto, api_key)
        texto_final += texto_corregido + "\n\n"
        
        if i < len(pages) - 1:
            time.sleep(2) # Para no sobrecargar la API

    doc = Document()
    for p in texto_final.split("\n"):
        if p.strip():
            doc.add_paragraph(p)

    doc.save(output_word)