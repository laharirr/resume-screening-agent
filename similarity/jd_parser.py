import re
from utils.constants import TECHNICAL_SKILLS


def parse_job_description(text):
    """
    Extract required skills from the job description.
    """
    found_skills = []

    lower_text = text.lower()

    for skill in TECHNICAL_SKILLS:
        if skill.lower() in lower_text:
            found_skills.append(skill)

    # Experience
    exp_match = re.search(r"(\d+)\s*[-+]?\s*(\d+)?\s*years?", lower_text)

    experience = exp_match.group() if exp_match else None

    return {
        "skills": sorted(list(set(found_skills))),
        "experience": experience,
        "raw_text": text,
    }