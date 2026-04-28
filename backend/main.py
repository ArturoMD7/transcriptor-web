from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from backend.ocr_service import procesar_pdf

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

UPLOAD_PATH = "temp.pdf"
OUTPUT_PATH = "resultado.docx"

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.post("/procesar")
async def procesar(
    file: UploadFile = File(...),
    pag_inicio: int = Form(1),
    pag_fin: int = Form(None)
):
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    procesar_pdf(UPLOAD_PATH, OUTPUT_PATH, pag_inicio, pag_fin)

    return FileResponse(
        OUTPUT_PATH,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="resultado.docx"
    )