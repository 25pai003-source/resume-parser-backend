#parser.py
import re
import pdfplumber

SKILLS = [
    "python",
    "sql",
    "flask",
    "machine learning",
    "html",
    "css",
    "javascript"
]

def read_resume(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    return text.lower()


def preprocess(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    return text.split()


def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return list(set(found))


def extract_experience(text):
    match = re.search(r"(\d+)\s+year", text)
    if match:
        return match.group(1) + " year(s)"
    return "Not mentioned"
