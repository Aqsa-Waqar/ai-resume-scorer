from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text: str) -> str:
    """Lowercase and remove special characters."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def score_resume(resume_text: str, job_description: str) -> dict:
    """
    Score how well a resume matches a job description.
    Uses TF-IDF vectorization + Cosine Similarity.
    """
    # Step 1: Clean both texts
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    # Step 2: TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([cleaned_resume, cleaned_jd])

    # Step 3: Cosine Similarity
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    score = round(float(similarity) * 100, 2)

    # Step 4: Find matched and missing keywords
    jd_words = set(cleaned_jd.split())
    resume_words = set(cleaned_resume.split())

    # Filter to meaningful words (length > 4)
    meaningful_jd_words = {w for w in jd_words if len(w) > 4}
    matched = meaningful_jd_words & resume_words
    missing = meaningful_jd_words - resume_words

    return {
        "score": score,
        "matched_keywords": sorted(list(matched))[:15],
        "missing_keywords": sorted(list(missing))[:15],
    }