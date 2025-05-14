# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
from .ai_client import summarize_and_structure, generate_quiz_from_manual
from PyPDF2 import PdfReader
import io
from app.flow import create_tutorial_flow
from app.utils.crawl_local_files import extract_file_content

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ─────────────────────────────────────────────────────────────────────
class FileContentResponse(BaseModel):
    files: Dict[str, str]

class ManualResponse(BaseModel):
    manual: str

class QuizQuestion(BaseModel):
    question: str
    answers: List[str]
    correctAnswer: List[int]

class Abstraction(BaseModel):
    """Represents a single abstraction in the output."""
    name: str = Field(..., description="The name of the abstraction.")
    description: str = Field(..., description="A beginner-friendly explanation of the abstraction.")
    files: List[int] = Field(..., description="List of file indices associated with this abstraction.")

class IdentifyAbstractionsOutput(BaseModel):
    """Represents the output of the IdentifyAbstractions Node."""
    abstractions: List[Abstraction] = Field(..., description="A list of identified abstractions.")

# ─── Health check ───────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "up!!"}


# ─── Manual endpoint with PocketFlow ────────────────────────────────────────────────────────────
@app.post("/api/manual_pocketflow", response_model=IdentifyAbstractionsOutput)
async def generate_manual(
    files: List[UploadFile] = File(..., description="Upload ≥2 PDF/TXT files"),
    prompt: str = Form(..., description="Prompt for manual generation")
):
    # Extract content from uploaded files
    try:
        files_content = []
        for file in files:
            content = await file.read()
            # Debug: Check the content length
            print(f"Processing file: {file.filename}, Content length: {len(content)}")
            if len(content) == 0:
                print(f"Skipping empty file: {file.filename}")
                continue

            # Convert content to UTF-8 and append to list
            files_content.append((file.filename, content.decode("utf-8", errors="ignore")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File processing failed: {e}")

    # Initialize shared store
    shared = {
        "files_content": files_content,
        "prompt": prompt,
        "use_cache": True,
        "max_abstraction_num": 5
    }

    # Create the flow instance
    tutorial_flow = create_tutorial_flow()

    # Execute the flow
    try:
        # If the flow contains any AsyncNode, use run_async()
       tutorial_flow.run(shared)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Manual generation failed: {e}")

    # Extract abstractions from the shared store
    abstractions = shared.get("abstractions", [])

    # Return the output structure
    return IdentifyAbstractionsOutput(abstractions=abstractions)


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
