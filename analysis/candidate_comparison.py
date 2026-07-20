import pandas as pd


def candidate_comparison(results):
    """
    Creates a recruiter-friendly comparison table.
    """

    df = pd.DataFrame(results)

    columns = [
        "candidate",
        "semantic_score",
        "skill_score",
        "final_score",
        "recommendation",
    ]

    return df[columns]