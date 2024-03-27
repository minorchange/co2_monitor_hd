from dash import html

import dash_bootstrap_components as dbc
from dash import dcc
import dash
import os
from components.colors import *

from datetime import datetime

proj_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(proj_dir)

from data.data import co2d
from components.container.container_details_budget import (
    create_container_details_budget,
)
from components.container.container_tldr import create_container_tldr
from components.custom_components.custom_tab_component import create_tabcomponent
from components.cards import header, footer

title_for_tab = "CO₂ Monitor Heidelberg"
app = dash.Dash(
    title=title_for_tab,
    update_title=None,
    external_stylesheets=[dbc.themes.SIMPLEX],
    suppress_callback_exceptions=True,
)

app, container_details_budget = create_container_details_budget(app)
app, container_tldr = create_container_tldr(app)


app, tabcomponent = create_tabcomponent(
    app,
    [
        ("Kurze Zusammenfassung", container_tldr),
        ("Details und Datengrundlage", container_details_budget),
    ],
)
app.layout = html.Div([header, tabcomponent])
# app.layout = html.Div([container_tldr, container_details_budget])

if __name__ == "__main__":
    app.run_server(debug=True)
