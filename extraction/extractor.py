from extraction.personal_info import extract_email, extract_phone
from extraction.skills import extract_skills
from extraction.education import extract_education
from extraction.experience import extract_experience
from extraction.certification import extract_certifications
from extraction.projects import extract_projects
from extraction.links import extract_linkedin, extract_github


def extract_resume_data(text):
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "certification": extract_certifications(text),
        "projects": extract_projects(text),
    }