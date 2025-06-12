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
        parsed = parser.parse_resume(resume_path) 

        # Match jobs
        matches = match_jobs(parsed["text"], parsed["skills"]) # from matcher.py

        # Remove temporary file
        os.remove(resume_path)

        return jsonify({
            "name": parsed["name"],
            "skills": parsed["skills"],
            "matched_jobs": matches
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
