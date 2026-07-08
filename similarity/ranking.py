from similarity.scorer import semantic_similarity


def rank_candidates(job_description, resumes):
    """
    Rank resumes based on semantic similarity to the JD.
    """

    ranked = []

    for filename, resume_text in resumes.items():

        score = semantic_similarity(job_description, resume_text)

        ranked.append({
            "candidate": filename,
            "score": round(score, 2)
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked