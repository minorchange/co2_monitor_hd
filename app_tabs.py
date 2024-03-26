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


# title_for_tab = "CO₂ Monitor Heidelberg"
# app = dash.Dash(
#     title=title_for_tab,
#     update_title=None,
#     external_stylesheets=[dbc.themes.SIMPLEX],
# )

title_for_tab = "CO₂ Monitor Heidelberg"
app = dash.Dash(
    title=title_for_tab,
    update_title=None,
    external_stylesheets=[dbc.themes.SIMPLEX],
)


import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize the Dash app
# app = dash.Dash(__name__)

# Define the layout
app, container_details_budget = create_container_details_budget(app)
# app, container_tldr = create_container_tldr(app)


# app, tabcomponent = create_tabcomponent(
#     app,
#     [("GAGA", "blubb"), ("Tab2", container_details_budget)],
# )
app.layout = container_details_budget
# app.layout = tabcomponent
# app.layout = html.Div(
#     [
#         html.H1("Welcome to My Dashboard"),
#         dcc.Tabs(
#             id="tabs",
#             value="welcome",
#             children=[
#                 dcc.Tab(label="Welcome", value="welcome"),
#                 dcc.Tab(label="Details", value="details"),
#             ],
#         ),
#         html.Div(id="tabs-content"),
#     ]
# )

# # Callback to switch between tabs
# @app.callback(Output("tabs-content", "children"), [Input("tabs", "value")])
# def render_content(tab):
#     if tab == "welcome":
#         return container_details_budget(app)
#         # return html.Div(
#         #     [
#         #         html.H3("Welcome to the Welcome Page"),
#         #         html.P(
#         #             "This is the welcome page. You can put whatever content you want here."
#         #         ),
#         #     ]
#         # )
#     elif tab == "details":
#         return html.Div(
#             [
#                 html.H3("Welcome to the Details Page"),
#                 html.P("This is the details page. You can put different content here."),
#             ]
#         )


if __name__ == "__main__":
    app.run_server(debug=True)
