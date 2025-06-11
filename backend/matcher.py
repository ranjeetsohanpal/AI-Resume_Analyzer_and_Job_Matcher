import json
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained model (lightweight + good accuracy)
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_jobs(path="jobs_db.json"):
    with open(path, 'r') as f:
        return json.load(f)


def match_jobs(resume_text, extracted_skills, top_n=3):
    jobs = load_jobs()
    job_texts = [job['description'] for job in jobs]

    # Encode resume and job descriptions
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embeddings = model.encode(job_texts, convert_to_tensor=True)

    # Compute cosine similarity
    cosine_scores = util.pytorch_cos_sim(resume_embedding, job_embeddings)[0]

    scored_jobs = []
    for i, score in enumerate(cosine_scores):
        job = jobs[i]
        required = set(map(str.lower, job.get("required_skills", [])))
        have = set(map(str.lower, extracted_skills))
        missing = required - have

        scored_jobs.append({
            "title": job["title"],
            "score": round(float(score) * 100, 2),
            "required_skills": job.get("required_skills", []),
            "missing_skills": list(missing)
        })

    # Sort and return top N
    scored_jobs.sort(key=lambda x: x['score'], reverse=True)
    return scored_jobs[:top_n]
