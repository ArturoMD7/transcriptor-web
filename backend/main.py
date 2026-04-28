from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from backend.ocr_service import procesar_pdf

app = FastAPI()

# CORS (para Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_PATH = "temp.pdf"
OUTPUT_PATH = "resultado.docx"

@app.get("/")
def home():
    return {"message": "API OCR funcionando"}

@app.post("/procesar")
async def procesar(
    file: UploadFile = File(...),
    pag_inicio: int = Form(1),
    pag_fin: int = Form(None)
):
    # Guardar archivo
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Procesar
    procesar_pdf(UPLOAD_PATH, OUTPUT_PATH, pag_inicio, pag_fin)

    return FileResponse(
        OUTPUT_PATH,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="resultado.docx"
    )