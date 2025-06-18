import json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_jobs(path="jobs_db.json"):
    with open(path, 'r') as f:
        return json.load(f)

def match_jobs(parsed_resume_json, top_n=3):
    """
    Takes parsed resume (dict or JSON) and returns top matching jobs in JSON format.
    Expected keys: 'text', 'skills'
    """
    resume_text = parsed_resume_json['summary']
    extracted_skills = parsed_resume_json['skills']

    if not resume_text or not extracted_skills:
        return {"error": "Missing resume text or skills in input."}

    jobs = load_jobs()
    job_texts = [job['description'] for job in jobs]

    # Encode text and compute similarity
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embeddings = model.encode(job_texts, convert_to_tensor=True)
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

    scored_jobs.sort(key=lambda x: x['score'], reverse=True)
    return {
        "matched_jobs": scored_jobs[:top_n]
    }




