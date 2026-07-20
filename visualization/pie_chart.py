import plotly.express as px
import pandas as pd


def recommendation_chart(results):

    df = pd.DataFrame(results)

    counts = (
        df["recommendation"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Recommendation",
        "Count"
    ]

    fig = px.pie(
        counts,
        names="Recommendation",
        values="Count",
        title="Recommendation Distribution",
    )

    return fig