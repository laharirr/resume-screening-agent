from utils.constants import TECHNICAL_SKILLS


def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in TECHNICAL_SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))