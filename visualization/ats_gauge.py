import plotly.graph_objects as go


def ats_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,

            title={
                "text": "ATS Match Score"
            },

            gauge={
                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "thickness": 0.35
                },

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "#ff4d4d"
                    },

                    {
                        "range": [40, 70],
                        "color": "#ffc107"
                    },

                    {
                        "range": [70, 100],
                        "color": "#28a745"
                    }

                ]
            }
        )
    )

    fig.update_layout(
        height=350
    )

    return fig