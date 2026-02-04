#parser.py
import nltk
import pdfplumber
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required nltk data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load skills list
with open("skills.txt", "r") as f:
    SKILLS = [skill.strip().lower() for skill in f.readlines()]


# ---------------------------------
# READ RESUME FILE
# ---------------------------------
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


# ---------------------------------
# PREPROCESS TEXT
# ---------------------------------
def preprocess(text):
    # Remove special characters
    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    words = text.split()

    # Remove stopwords + lemmatize
    processed_words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return processed_words


# ---------------------------------
# EXTRACT SKILLS
# ---------------------------------
def extract_skills(words):
    found_skills = set()

    for word in words:
        if word in SKILLS:
            found_skills.add(word)

    return list(found_skills)


# ---------------------------------
# COMPLETE PIPELINE FUNCTION
# ---------------------------------
def parse_resume(file_path):

    # Step 1: Read resume
    text = read_resume(file_path)

    # Step 2: Preprocess text
    processed_words = preprocess(text)

    # Step 3: Extract skills
    skills = extract_skills(processed_words)

    return {
        "skills": skills,
        "text": text
    }
