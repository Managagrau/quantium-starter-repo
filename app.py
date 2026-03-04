import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("data/pink_morsels.csv")

# normalize columns (handles Sales/Date/Region vs sales/date/region)
df.columns = [c.strip().lower() for c in df.columns]
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

REGIONS = ["all", "north", "east", "south", "west"]

app = Dash(__name__)

app.layout = html.Div(
    style={
        "background": "linear-gradient(135deg, #f7f7ff, #eef6ff)",
        "minHeight": "100vh",
    },
    children=[
        html.Div(
            style={
                "fontFamily": "Arial",
                "maxWidth": "1000px",
                "margin": "0 auto",
                "padding": "24px",
            },
            children=[
                html.Div(
            style={
                "backgroundColor": "white",
                "padding": "18px 20px",
                "borderRadius": "16px",
                "boxShadow": "0 10px 25px rgba(0,0,0,0.08)",
                "marginBottom": "18px",
            },
                    children=[
                        html.H1(
                            "Pink Morsel Sales Visualiser",
                            style={"margin": "0 0 6px 0", "textAlign": "center"},
                        ),
                        html.P(
                            "Filter by region to explore Pink Morsel sales over time.",
                            style={"margin": "0", "textAlign": "center", "color": "#444"},
                        ),
                    ],
                ),

                html.Div(
            style={
                "backgroundColor": "white",
                "padding": "14px 18px",
                "borderRadius": "16px",
                "boxShadow": "0 10px 25px rgba(0,0,0,0.08)",
                "marginBottom": "18px",
            },
                    children=[
                        html.Div(
                            "Region",
                            style={"fontWeight": "bold", "marginBottom": "10px"},
                        ),
                        dcc.RadioItems(
                            id="region",
                            options=[{"label": r.title(), "value": r} for r in REGIONS],
                            value="all",
                            inline=True,
                            style={"display": "flex", "gap": "14px", "flexWrap": "wrap"},
                            inputStyle={"marginRight": "6px"},
                        ),
                    ],
                ),

                html.Div(
            style={
                "backgroundColor": "white",
                "padding": "14px 18px",
                "borderRadius": "16px",
                "boxShadow": "0 10px 25px rgba(0,0,0,0.08)",
            },
                    children=[
                        dcc.Graph(id="sales-chart", config={"displayModeBar": False}),
                    ],
                ),
            ],
        ),
    ],
)

@app.callback(
    Output("sales-chart", "figure"),
    Input("region", "value"),
)
def update_chart(region):
    if region == "all":
        dff = df.copy()
        title = "Pink Morsel Sales — All Regions"
    else:
        dff = df[df["region"].str.lower() == region].copy()
        title = f"Pink Morsel Sales — {region.title()}"

    # (Optional but helpful) total sales per day for the selected region
    dff["sales"] = pd.to_numeric(dff["sales"], errors="coerce")
    daily = dff.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    fig = px.line(
        daily,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Total Sales"},
        title=title,
    )

    fig.update_layout(
        margin=dict(l=30, r=20, t=60, b=30),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.06)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.06)")

    return fig

if __name__ == "__main__":
    app.run()
