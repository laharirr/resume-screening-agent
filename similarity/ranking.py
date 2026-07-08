from extraction.extractor import extract_resume_data

from similarity.scorer import semantic_similarity
from similarity.hybrid_score import skill_score, final_score
from similarity.jd_parser import parse_job_description


def rank_candidates(job_description, resumes):
    """
    Rank resumes using semantic similarity + skill matching.
    """

    # Parse the Job Description
    jd = parse_job_description(job_description)

    results = []

    # Process each resume
    for filename, resume_text in resumes.items():

        # Extract candidate information
        candidate = extract_resume_data(resume_text)

        # Calculate semantic similarity
        semantic = semantic_similarity(job_description, resume_text)

        # Calculate skill match
        skills = skill_score(
            candidate["skills"],
            jd["skills"]
        )

        # Calculate final score
        score = final_score(
            semantic,
            skills
        )

        # Store result
        results.append({
            "candidate": filename,
            "semantic_score": round(semantic, 2),
            "skill_score": round(skills, 2),
            "final_score": round(score, 2)
        })

    # Sort by highest score
    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return results