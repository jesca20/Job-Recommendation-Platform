import fitz  # from PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    skills_db = [
    'python', 'java', 'javascript', 'html', 'css', 'react', 'angular', 'vue.js',
    'redux', 'jquery', 'node.js', 'express.js', 'django', 'flask', 'spring boot',
    'sql', 'mysql', 'postgresql', 'mongodb', 'git', 'docker', 'kubernetes', 'aws',
    'azure', 'google cloud', 'rest api', 'graphql', 'tensorflow', 'pytorch',
    'scikit-learn', 'pandas', 'numpy', 'tableau', 'power bi', 'adobe photoshop',
    'figma', 'ui/ux design', 'agile', 'devops', 'cybersecurity', 'communication',
    'leadership', 'teamwork', 'problem-solving', 'critical thinking', 'creativity',
    'time management', 'adaptability', 'attention to detail', 'organization'
]
    text = text.lower()
    return [skill for skill in skills_db if skill in text]
