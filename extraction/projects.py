import re


PROJECT_KEYWORDS = [
    "project",
    "developed",
    "built",
    "implemented",
    "created"
]


def extract_projects(text):

    projects = []

    lines = text.split("\n")

    for line in lines:

        for word in PROJECT_KEYWORDS:

            if word.lower() in line.lower():
                projects.append(line.strip())

    return list(set(projects))