import re

EDUCATION_KEYWORDS = [
    "b.e",
    "b.tech",
    "bachelor",
    "m.tech",
    "m.e",
    "master",
    "phd",
    "computer science",
    "information science",
    "data science",
    "artificial intelligence"
]


def extract_education(text):

    education = []

    lower = text.lower()

    for item in EDUCATION_KEYWORDS:
        if item in lower:
            education.append(item.title())

    return sorted(list(set(education)))