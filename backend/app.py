from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import ResumeParser
from matcher import match_jobs
import os
import tempfile
app = Flask(__name__) # declare the application
CORS(app)  # allow requests from react

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        print("❌ No file found in request.")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    print(f"✅ Received file: {file.filename}")
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            file.save(tmp.name)
            resume_path = tmp.name

        # Parse the resume from the file path
        parser = ResumeParser()
        parsed_resume = parser.parse_resume(resume_path) 

        # Remove temporary file
        os.remove(resume_path)

        # Run job matcher
        top_n = 3

        parsed_dict = {
            'summary' : parsed_resume.summary,
            'skills' : parsed_resume.skills
        }
        matched = match_jobs(parsed_dict,top_n=top_n)
        titles = []
        scores = []
        req_skills = []
        missing_skills = []
        
        for i in range(top_n):
            titles.append(matched['matched_jobs'][i]['title'])
            scores.append(matched['matched_jobs'][i]['score'])
            req_skills.append(matched['matched_jobs'][i]['required_skills'])
            missing_skills.append(matched['matched_jobs'][i]['missing_skills'])
        return jsonify({
            "name": parsed_resume.contact_info.name,
            "skills": parsed_resume.skills,
            "summary" : parsed_resume.summary,
            "matched_job_titles" : titles,
            "sim_scores" : scores,
            "req_skills" : req_skills,
            "missing_skills" : missing_skills
        }) 
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
