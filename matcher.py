#matcher.py
def match_resume(resume_skills, job_skills):
    if len(job_skills) == 0:
        return 0

    common = set(resume_skills).intersection(set(job_skills))
    score = (len(common) / len(job_skills)) * 100
    return round(score, 2)
