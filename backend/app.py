# app.py (backend main file)
from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import ResumeParser
from matcher import match_jobs

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    parser = ResumeParser
    parsed = parser.parse_resume(file)
    matches = match_jobs(parsed["text"], parsed["skills"])

    return jsonify({
        "name": parsed["name"],
        "skills": parsed["skills"],
        "matched_jobs": matches
    })

if __name__ == "__main__":
    app.run(debug=True)
