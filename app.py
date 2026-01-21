#app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parser import read_resume, preprocess, extract_skills, extract_experience
from matcher import match_resume

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ------------------------------
# API 1: Upload & Parse Resume
# ------------------------------
@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Read and parse resume
    text = read_resume(file_path)
    tokens = preprocess(text)
    skills = extract_skills(text)
    experience = extract_experience(text)

    return jsonify({
        "filename": file.filename,
        "skills": skills,
        "experience": experience
    })


# ---------------------------------
# API 2: Match Resume with Job Desc
# ---------------------------------
@app.route("/match", methods=["POST"])
def match():
    data = request.json

    resume_skills = data.get("resume_skills", [])
    job_description = data.get("job_description", "").lower()

    # Extract job skills
    job_skills = []
    from parser import SKILLS
    for skill in SKILLS:
        if skill in job_description:
            job_skills.append(skill)

    score = match_resume(resume_skills, job_skills)

    return jsonify({
        "job_skills": job_skills,
        "match_score": score
    })


# ------------------------------
# Run Server
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)





