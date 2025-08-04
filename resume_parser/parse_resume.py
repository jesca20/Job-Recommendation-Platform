import fitz  # from PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    skills_db = ['python', 'sql', 'aws', 'docker', 'pandas', 'java', 'git', 'airflow']
    text = text.lower()
    return [skill for skill in skills_db if skill in text]
