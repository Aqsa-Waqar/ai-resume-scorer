from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_text_from_pdf
from scorer import score_resume
from dotenv import load_dotenv
import os
import io

load_dotenv()

app = FastAPI(title="AI Resume Scorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ai_feedback(resume_text: str, job_description: str, matching: list, missing: list) -> dict:
    
    jd_lower = job_description.lower()
    resume_lower = resume_text.lower()
    
    recommendations = []
    
    if missing:
        recommendations.append(f"Add these missing keywords to your resume: {', '.join(missing[:5])}")
    
    if "java" in jd_lower and "java" not in resume_lower:
        recommendations.append("Consider learning Java basics — it is required for this role")
    
    if "python" in jd_lower and "python" in resume_lower:
        recommendations.append("Expand your Python experience with specific libraries and projects")
    
    if "communication" in jd_lower:
        recommendations.append("Add a line about teamwork or communication in your summary section")
    
    if "sql" in jd_lower and "sql" in resume_lower:
        recommendations.append("Mention specific SQL queries or database operations you have performed")

    if "machine learning" in jd_lower or "ml" in jd_lower:
        recommendations.append("Highlight any ML or AI projects prominently at the top of your resume")

    if "rest api" in jd_lower and "rest" in resume_lower:
        recommendations.append("Describe the REST APIs you built — mention endpoints, methods, and purpose")

    recommendations.append("Quantify your achievements — add numbers and measurable impact to bullet points")
    recommendations.append("Tailor your summary section specifically to mention this role and company")

    score_val = len(matching) / max(len(missing) + len(matching), 1) * 100
    ats_score = min(int(score_val) + 20, 95)

    experience_analysis = f"Your resume shows {len(matching)} matching skills for this role. "
    if len(missing) > 5:
        experience_analysis += "There are several skill gaps to address. Focus on your most relevant projects and highlight transferable skills."
    elif len(missing) > 2:
        experience_analysis += "You have a partial match. Highlight your relevant projects and emphasize transferable skills."
    else:
        experience_analysis += "Strong alignment with the job requirements! Make sure your summary reflects this match clearly."

    overall = f"Based on keyword and skill analysis, your resume matches approximately {ats_score}% of this job's requirements. "
    if missing:
        overall += f"Priority areas to address: {', '.join(missing[:3])}. "
    overall += "Tailor your resume specifically for this role to maximize your chances of getting shortlisted."

    return {
        "ats_score": ats_score,
        "experience_analysis": experience_analysis,
        "recommendations": recommendations[:5],
        "overall_assessment": overall
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
    ai_result = get_ai_feedback(
        resume_text,
        job_description,
        tfidf_result["matched_keywords"],
        tfidf_result["missing_keywords"]
    )

    return {
        "score": tfidf_result["score"],
        "ats_score": ai_result["ats_score"],
        "matching_skills": tfidf_result["matched_keywords"],
        "missing_keywords": tfidf_result["missing_keywords"],
        "experience_analysis": ai_result["experience_analysis"],
        "recommendations": ai_result["recommendations"],
        "overall_assessment": ai_result["overall_assessment"]
    }