from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_text_from_pdf
from scorer import score_resume
from dotenv import load_dotenv
from google import genai
import os
import io
import json

load_dotenv()

app = FastAPI(title="AI Resume Scorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_feedback(resume_text: str, job_description: str, score: float) -> dict:
    prompt = f"""You are an expert ATS analyzer and professional resume coach.

Analyze this resume against the job description and respond in EXACTLY this JSON format, no other text:

{{
  "ats_score": <number 0-100>,
  "matching_skills": ["skill1", "skill2", "skill3"],
  "missing_keywords": ["keyword1", "keyword2", "keyword3"],
  "experience_analysis": "2-3 sentences about experience alignment",
  "recommendations": [
    "specific tip 1",
    "specific tip 2",
    "specific tip 3",
    "specific tip 4",
    "specific tip 5"
  ],
  "overall_assessment": "2-3 sentence professional summary tailored to this job"
}}

Resume: {resume_text[:1200]}

Job Description: {job_description[:1000]}

Return ONLY the JSON object, nothing else."""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Gemini error: {e}")
        return {
            "ats_score": 0,
            "matching_skills": [],
            "missing_keywords": [],
            "experience_analysis": "Could not analyze experience.",
            "recommendations": ["Add more keywords from job description"],
            "overall_assessment": "Please try again."
        }


@app.get("/")
def root():
    return {"message": "AI Resume Scorer API is running!"}


@app.post("/score")
async def score(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    pdf_bytes = await resume.read()
    pdf_file = io.BytesIO(pdf_bytes)
    resume_text = extract_text_from_pdf(pdf_file)

    if not resume_text:
        return {"error": "Could not extract text from PDF."}

    tfidf_result = score_resume(resume_text, job_description)
    ai_result = get_ai_feedback(resume_text, job_description, tfidf_result["score"])

    return {
        "score": tfidf_result["score"],
        "ats_score": ai_result["ats_score"],
        "matching_skills": ai_result["matching_skills"],
        "missing_keywords": ai_result["missing_keywords"],
        "experience_analysis": ai_result["experience_analysis"],
        "recommendations": ai_result["recommendations"],
        "overall_assessment": ai_result["overall_assessment"]
    }