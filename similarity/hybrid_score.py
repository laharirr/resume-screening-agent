def skill_score(candidate_skills, jd_skills):
    """
    Calculate percentage of required skills matched.
    """
    if not jd_skills:
        return 100.0

    matched = set(candidate_skills).intersection(set(jd_skills))

    return (len(matched) / len(jd_skills)) * 100


def final_score(semantic, skill):
    """
    Temporary weighted score.
    """
    return round(
        semantic * 0.70 +
        skill * 0.30,
        2
    )

