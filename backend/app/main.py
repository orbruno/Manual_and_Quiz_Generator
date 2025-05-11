# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from .ai_client import summarize_and_structure, generate_quiz_from_manual
from PyPDF2 import PdfReader
import io

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ─────────────────────────────────────────────────────────────────────
class ManualResponse(BaseModel):
    manual: str

class QuizQuestion(BaseModel):
    question: str
    answers: List[str]
    correctAnswer: List[int]

# ─── Health check ───────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "up"}

# ─── Manual endpoint ────────────────────────────────────────────────────────────
@app.post("/api/manual", response_model=ManualResponse)
async def generate_manual(
    files: List[UploadFile] = File(..., description="Upload ≥2 PDF/TXT files"),
    prompt: str = Form(..., description="Prompt for manual generation")
):
    # 1) extract text
    texts: List[str] = []
    for upload in files:
        data = await upload.read()
        if upload.filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(data))
            pages = [page.extract_text() or "" for page in reader.pages]
            texts.append("\n\n".join(pages))
        else:
            texts.append(data.decode("utf-8", errors="ignore"))

    # 2) generate manual
    try:
        manual = summarize_and_structure(texts, prompt)
    except Exception as e:
        raise HTTPException(500, f"Manual generation failed: {e}")

    return ManualResponse(manual=manual)

# ─── Quiz endpoint ──────────────────────────────────────────────────────────────
@app.post("/api/quiz", response_model=List[QuizQuestion])
async def generate_quiz(
    payload: Dict = Body(..., example={"manual": "<your HTML or Markdown here>"}),
):
    manual = payload.get("manual")
    if not manual:
        raise HTTPException(400, "`manual` field is required")

    try:
        quiz_list = generate_quiz_from_manual(manual)
    except Exception as e:
        raise HTTPException(500, f"Quiz generation failed: {e}")

    return quiz_list
