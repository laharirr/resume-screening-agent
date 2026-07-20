import re


def extract_linkedin(text):

    pattern = r"https?://(www\.)?linkedin\.com/[^\s]+"

    match = re.search(pattern, text)

    return match.group() if match else None


def extract_github(text):

    pattern = r"https?://(www\.)?github\.com/[^\s]+"

    match = re.search(pattern, text)

    return match.group() if match else None