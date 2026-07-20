import plotly.graph_objects as go


def skill_radar(candidate_skills, jd_skills):

    categories = sorted(list(set(jd_skills)))

    values = []

    for skill in categories:
        if skill in candidate_skills:
            values.append(1)
        else:
            values.append(0)

    # close the radar
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Candidate"
        )
    )

    fig.update_layout(

        title="Skill Match Radar",

        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,1]
            )
        ),

        showlegend=False,
        height=500
    )

    return fig