import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

df = pd.read_csv("data/pink_morsels.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "maxWidth": "900px",
        "margin": "auto",
        "padding": "20px"
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center"}
        ),
        dcc.Graph(
            figure=px.line(
                df,
                x="Date",
                y="Sales",
                labels={"Date": "Date", "Sales": "Sales"}
            )
        )
    ]
)

if __name__ == "__main__":
    app.run()