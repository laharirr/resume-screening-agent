from extraction.personal_info import extract_email, extract_phone
from extraction.skills import extract_skills


def extract_resume_data(text):
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
    }