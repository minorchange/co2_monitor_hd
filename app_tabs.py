# import dash_html_components as html
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash
# import os
# from colors import *

# from datetime import datetime


# proj_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(proj_dir)


# from data.data import co2d


# title_for_tab = "CO₂ Monitor Heidelberg"
# app = dash.Dash(
#     title=title_for_tab,
#     update_title=None,
#     external_stylesheets=[dbc.themes.SIMPLEX],
# )


# from cards import (
#     header,
#     card_main_compare,
#     card_paris,
#     card_diff_year,
#     card_faq,
#     card_about,
#     card_table_compare_plans,
#     card_table_budgets,
# )

# app, main_compare = card_main_compare(app, co2d)
# app, card_paris = card_paris(app, co2d)
# card_diff_year = card_diff_year(app, co2d)
# card_faq = card_faq(app, co2d)
# card_about = card_about()
# card_table_compare_plans = card_table_compare_plans(app, co2d)
# app, card_table_budgets = card_table_budgets(app, co2d)


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    [
        html.H1("Welcome to My Dashboard"),
        dcc.Tabs(
            id="tabs",
            value="welcome",
            children=[
                dcc.Tab(label="Welcome", value="welcome"),
                dcc.Tab(label="Details", value="details"),
            ],
        ),
        html.Div(id="tabs-content"),
    ]
)


# Callback to switch between tabs
@app.callback(Output("tabs-content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "welcome":
        return html.Div(
            [
                html.H3("Welcome to the Welcome Page"),
                html.P(
                    "This is the welcome page. You can put whatever content you want here."
                ),
            ]
        )
    elif tab == "details":
        return html.Div(
            [
                html.H3("Welcome to the Details Page"),
                html.P("This is the details page. You can put different content here."),
            ]
        )


if __name__ == "__main__":
    app.run_server()
