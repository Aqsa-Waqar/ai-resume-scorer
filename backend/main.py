from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_text_from_pdf
from scorer import score_resume
from dotenv import load_dotenv
import requests
import os
import io

load_dotenv()

app = FastAPI(title="AI Resume Scorer API")

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ai_feedback(resume_text: str, job_description: str, score: float) -> str:
    token = os.getenv("HF_API_TOKEN")
    
    prompt = f"Give 3 tips to improve this resume for the job. Resume skills: {resume_text[:300]} Job requires: {job_description[:200]} Match score: {score}%. Tips:"

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers=headers,
            json=payload,
            timeout=30
        )
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()
        else:
            return "Tip 1: Add missing keywords from the job description.\nTip 2: Quantify your achievements with numbers.\nTip 3: Tailor your summary to match the role."
    except Exception:
        return "Tip 1: Add missing keywords from the job description.\nTip 2: Quantify your achievements with numbers.\nTip 3: Tailor your summary to match the role."

@app.get("/")
def root():
    return {"message": "AI Resume Scorer API is running!"}


@app.post("/score")
async def score(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Read uploaded PDF into memory
    pdf_bytes = await resume.read()
    pdf_file = io.BytesIO(pdf_bytes)

    # Extract text
    resume_text = extract_text_from_pdf(pdf_file)

    if not resume_text:
        return {"error": "Could not extract text from PDF. Make sure it's not a scanned image."}

    # Score it
    result = score_resume(resume_text, job_description)

    # Get AI feedback
    feedback = get_ai_feedback(resume_text, job_description, result["score"])
    result["feedback"] = feedback

    return result