#parser.py
import nltk
import pdfplumber
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load skills list
with open("skills.txt", "r") as f:
    SKILLS = [skill.strip().lower() for skill in f.readlines()]


def read_resume(file_path):
    """Read PDF or TXT resume"""
    text = ""

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    return text.lower()


def preprocess(text):
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if w.isalpha()]
    tokens = [w for w in tokens if w not in stop_words]
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return tokens


def extract_skills(text):
    found_skills = set()
    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)
    return list(found_skills)


def extract_experience(text):
    matches = re.findall(r'(\d+)\s+years', text)
    if matches:
        return max(matches)
    return "Not mentioned"

