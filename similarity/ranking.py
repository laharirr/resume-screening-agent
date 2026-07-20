from extraction.extractor import extract_resume_data
from similarity.scorer import semantic_similarity
from similarity.hybrid_score import skill_score, final_score
from similarity.jd_parser import parse_job_description


def rank_candidates(job_description, resumes):

    print("STEP 1 -> Parsing JD")

    jd = parse_job_description(job_description)

    print("JD Skills:", jd["skills"])

    results = []

    for filename, resume_text in resumes.items():

        print("=" * 60)
        print("Processing:", filename)

        print("STEP 2 -> Extracting Resume")
        candidate = extract_resume_data(resume_text)

        print("Skills Found:", candidate["skills"])

        print("STEP 3 -> Semantic Similarity")
        semantic = semantic_similarity(
            job_description,
            resume_text
        )

        logger.info(f"Semantic Score: {semantic}")

        print("STEP 4 -> Skill Score")
        skills = skill_score(
            candidate["skills"],
            jd["skills"]
        )

        print("Skill:", skills)

        print("STEP 5 -> Final Score")
        score = final_score(
            semantic,
            skills
        )

        print("Final:", score)

        results.append(
            {
                "candidate": filename,
                "semantic_score": round(semantic,2),
                "skill_score":round(skills,2),
                "final_score":round(score,2),
                "recommendation":"Recommended"
                if score>=70
                else "Not Recommended"
            }
        )

    results.sort(
        key=lambda x:x["final_score"],
        reverse=True
    )

    from utils.logger import logger

    logger.info("Ranking Complete")

    return results