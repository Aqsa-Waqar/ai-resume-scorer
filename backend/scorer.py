from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Words to ignore even if they appear important
IGNORE_WORDS = {
    'looking', 'basic', 'other', 'about', 'with', 'that', 'this',
    'will', 'have', 'from', 'they', 'been', 'were', 'their', 'what',
    'when', 'which', 'your', 'into', 'more', 'also', 'each', 'just',
    'every', 'based', 'using', 'used', 'ability', 'aligns', 'assist',
    'attention', 'bricks', 'building', 'clients', 'collaborate',
    'agency', 'businesses', 'real', 'world', 'hands', 'work'
}

# Keywords that are always important in tech jobs
TECH_KEYWORDS = {
    'python', 'javascript', 'react', 'nodejs', 'sql', 'html', 'css',
    'machine learning', 'api', 'restapi', 'fastapi', 'flask', 'django',
    'docker', 'git', 'github', 'aws', 'azure', 'cloud', 'database',
    'mongodb', 'postgresql', 'typescript', 'nextjs', 'vuejs',
    'bubble', 'bubbleio', 'nocode', 'lowcode', 'figma', 'postman',
    'testing', 'debugging', 'agile', 'scrum', 'communication',
    'teamwork', 'internship', 'fullstack', 'frontend', 'backend',
    'opencv', 'numpy', 'pytorch', 'tensorflow', 'cpp', 'java'
}

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_keywords(text: str) -> set:
    cleaned = clean_text(text)
    words = set(cleaned.split())
    # Keep words that are either tech keywords or longer than 5 chars and not in ignore list
    meaningful = {
        w for w in words
        if (w in TECH_KEYWORDS or (len(w) > 5 and w not in IGNORE_WORDS))
    }
    return meaningful

def score_resume(resume_text: str, job_description: str) -> dict:
    # TF-IDF Cosine Similarity for overall score
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    score = round(float(similarity) * 100, 2)

    # Smart keyword matching
    jd_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)

    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords

    # Sort by importance (tech keywords first)
    def sort_key(w):
        return (0 if w in TECH_KEYWORDS else 1, w)

    return {
        "score": score,
        "matched_keywords": sorted(list(matched), key=sort_key)[:15],
        "missing_keywords": sorted(list(missing), key=sort_key)[:15],
    }