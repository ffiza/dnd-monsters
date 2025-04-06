from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import os

from data import generate_dummy_data

df = generate_dummy_data(n_data=50)

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Graphs
fig = px.scatter(df, x="Strength", y="Dexterity")

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dungeons & Dragons 5th Edition Monsters"),
                style={"textAlign":  "center",
                       "fontSize": 24},
                width={"size": 8, "offset": 2})
    ]),
    dbc.Row([
        dbc.Col(html.P("Text description"),
                style={"textAlign":  "left",
                       "fontSize": 18},
                width={"size": 8, "offset": 2})
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig),
                width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig),
                width=4),
        dbc.Col(dcc.Graph(figure=fig),
                width=4),
        dbc.Col([
            dbc.Row(html.H4("Creature Name"),
                    style={"textAlign": "center"}),
            dbc.Row(dcc.Graph(figure=fig)),
            dbc.Row(dcc.Graph(figure=fig)),
            dbc.Row(dcc.Graph(figure=fig)),
        ], width=4)
    ])
])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=True)
