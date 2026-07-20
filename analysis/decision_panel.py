def recruiter_decision(candidate, report):

    score = candidate["final_score"]

    matched = report["Matched Skills"]
    missing = report["Missing Skills"]

    if score >= 85:
        decision = "🟢 Strong Hire"
        interview = "Proceed to Technical Interview"

    elif score >= 70:
        decision = "🟡 Hire"
        interview = "Technical + HR Interview"

    elif score >= 50:
        decision = "🟠 Consider"
        interview = "Screen Further"

    else:
        decision = "🔴 Reject"
        interview = "Not Recommended"

    strength = (
        ", ".join(matched)
        if matched else "No major strengths identified"
    )

    weakness = (
        ", ".join(missing)
        if missing else "No missing skills"
    )

    return {
        "Decision": decision,
        "Strength": strength,
        "Weakness": weakness,
        "Interview": interview,
        "ATS": score
    }