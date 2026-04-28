from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
from ocr_service import procesar_pdf

app = FastAPI()

UPLOAD_PATH = "temp.pdf"
OUTPUT_PATH = "resultado.docx"

@app.get("/")
def home():
    return {"message": "API OCR funcionando"}

@app.post("/procesar")
async def procesar(file: UploadFile = File(...)):
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    procesar_pdf(UPLOAD_PATH, OUTPUT_PATH)

    return FileResponse(
        OUTPUT_PATH,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="resultado.docx"
    )