def generate_report(candidate, jd_skills, recommendation):
    """
    Generate recruiter-friendly analysis.
    """

    candidate_skills = set(candidate["skills"])
    required_skills = set(jd_skills)

    matched = sorted(candidate_skills.intersection(required_skills))
    missing = sorted(required_skills.difference(candidate_skills))

    if len(required_skills) > 0:
        match_percentage = round(
            (len(matched) / len(required_skills)) * 100,
            2,
        )
    else:
        match_percentage = 100

    report = {
        "Matched Skills": matched,
        "Missing Skills": missing,
        "Match Percentage": match_percentage,
        "Recommendation": recommendation,
    }

    return report
