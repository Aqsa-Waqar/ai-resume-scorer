# 🎯 AI Resume Scorer

An intelligent ATS (Applicant Tracking System) resume analyzer that scores your resume against any job description using Machine Learning and Google Gemini AI.

![AI Resume Scorer](https://img.shields.io/badge/AI-Resume%20Scorer-6366f1?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

## 🌐 Live Demo
🔗 **App:** [ai-resume-scorer.vercel.app](https://ai-resume-scorer.vercel.app)  
🔗 **API:** [aqsa-waqar-ai-resume-scorer-api.hf.space](https://aqsa-waqar-ai-resume-scorer-api.hf.space)  
📖 **API Docs:** [aqsa-waqar-ai-resume-scorer-api.hf.space/docs](https://aqsa-waqar-ai-resume-scorer-api.hf.space/docs)

---

## 🧠 What It Does

Upload your resume (PDF) and paste any job description — the app will instantly tell you:

- ✅ **ATS Match Score** (0-100) — how well your resume matches the job
- ✅ **Matched Keywords** — skills you already have that the job wants
- ❌ **Missing Keywords** — important skills you need to add
- 📊 **Experience Analysis** — how your projects align with the role
- 💡 **Actionable Recommendations** — specific tips to improve your resume
- 📋 **Overall Assessment** — a tailored professional summary

---

## 🔬 ML Concepts Used

| Concept | How It's Used |
|---|---|
| **TF-IDF Vectorization** | Converts resume and job description text into numerical vectors |
| **Cosine Similarity** | Measures how closely the resume matches the job description |
| **NLP Preprocessing** | Tokenization, stop word removal, text cleaning |
| **LLM (Gemini AI)** | Generates intelligent, human-readable feedback and analysis |

---

## 🏗️ Architecture
User (Browser)
↓
React Frontend (Vercel)
↓
FastAPI Backend (Hugging Face Spaces)
↓
┌─────────────────────────────────┐
│  1. PDF Text Extraction         │
│     (pdfplumber)                │
│  2. TF-IDF Vectorization        │
│     (scikit-learn)              │
│  3. Cosine Similarity Score     │
│     (scikit-learn)              │
│  4. Gemini AI Analysis          │
│     (google-genai)              │
└─────────────────────────────────┘
↓
Results: Score + Keywords + AI Feedback

---

## 🛠️ Tech Stack

**Backend**
- Python 3.10
- FastAPI
- pdfplumber (PDF text extraction)
- scikit-learn (TF-IDF + Cosine Similarity)
- Google Gemini AI (intelligent feedback)
- Hosted on Hugging Face Spaces 🤗

**Frontend**
- React.js
- Axios
- CSS3
- Hosted on Vercel

---

## 🚀 Run Locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:
GEMINI_API_KEY=your_gemini_api_key
HF_API_TOKEN=your_huggingface_token

Get your free Gemini API key at: [aistudio.google.com](https://aistudio.google.com)

```bash
uvicorn main:app --reload
```

API runs at: `http://localhost:8000`  
API Docs at: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm start
```

App runs at: `http://localhost:3000`

---

## 📁 Project Structure
ai-resume-scorer/
├── backend/
│   ├── main.py          # FastAPI app + Gemini integration
│   ├── scorer.py        # TF-IDF + Cosine Similarity logic
│   ├── extractor.py     # PDF text extraction
│   ├── Dockerfile       # For Hugging Face deployment
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   └── App.css      # Styling
│   └── package.json
└── README.md

---

## 💡 What I Learned

- How **TF-IDF** works to represent text as numerical vectors
- How **Cosine Similarity** measures document similarity
- Building and deploying a **REST API** with FastAPI
- Integrating **Large Language Models** via API
- Deploying ML models on **Hugging Face Spaces**
- Full stack development with **React + FastAPI**
- The importance of **.gitignore** for keeping secrets safe 😄

---

## 🔮 Future Improvements

- Support for DOCX resume format
- LinkedIn profile URL analysis
- Multi-language support (Urdu resume analysis)
- Resume rewriting suggestions with one click
- Save and compare multiple job applications

---

## 👩‍💻 Author

**Aqsa Waqar**  
BS Information Technology — FCIT, University of Punjab  
[LinkedIn](https://www.linkedin.com/in/aqsa-waqar025) | [GitHub](https://github.com/Aqsa-Waqar)

---

## 📄 Dataset & Tools

- **Dataset:** User-provided resumes and job descriptions (real-world data)
- **Libraries:** scikit-learn, pdfplumber, FastAPI, google-genai, React
- **Hosting:** Hugging Face Spaces (backend), Vercel (frontend)
