import re


def extract_experience(text):

    pattern = r"(\d+)\+?\s*(years|year|yrs|yr)"

    matches = re.findall(pattern, text.lower())

    if not matches:
        return 0

    years = [int(match[0]) for match in matches]

    return max(years)