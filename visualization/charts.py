import plotly.express as px
import pandas as pd


def score_chart(results):
    df = pd.DataFrame(results)

    fig = px.bar(
        df,
        x="candidate",
        y="final_score",
        color="final_score",
        title="Candidate Ranking",
        text="final_score",
    )

    fig.update_layout(
        xaxis_title="Candidate",
        yaxis_title="Final Score",
    )

    return fig