from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from model_loader import generate_summary
from fastapi.middleware.cors import CORSMiddleware

from pdfminer.high_level import extract_text

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Backend is running successfully"}


@app.on_event("startup")
async def startup():
    print("Server started successfully")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    return {"file_id": file.filename}

@app.post("/summarize")
async def summarize(file_id: str):
    path = os.path.join(UPLOAD_DIR, file_id)
    
    print("Checking:", path)
    print("Exists:", os.path.exists(path))

    if not os.path.exists(path):
        return JSONResponse({"error":"not found"},404)

    from pdfminer.high_level import extract_text
    text = extract_text(path)

    summary = generate_summary(text[:3000])
    
    summary_filename = file_id.replace(".pdf", "summary.txt")

    summary_path = os.path.join(UPLOAD_DIR, summary_filename)
    
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    return {"summary": summary}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)