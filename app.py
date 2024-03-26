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


title_for_tab = "CO₂ Monitor Heidelberg"
app = dash.Dash(
    title=title_for_tab,
    update_title=None,
    external_stylesheets=[dbc.themes.SIMPLEX],
)


from components.cards import (
    header,
    create_card_main_compare,
    create_card_paris,
    create_card_diff_year,
    create_card_faq,
    card_imprint,
    create_card_table_compare_plans,
    create_card_table_budgets,
)

app, main_compare = create_card_main_compare(app, co2d)
app, card_paris = create_card_paris(app, co2d)
card_diff_year = create_card_diff_year(app, co2d)
card_faq = create_card_faq(app, co2d)
card_about = card_imprint()
card_table_compare_plans = create_card_table_compare_plans(app, co2d)
app, card_table_budgets = create_card_table_budgets(app, co2d)


# container_details_budget = html.Div(
#     [
#         header,
#         dbc.Container(
#             [
#                 html.P(),
#                 dbc.Row(
#                     [
#                         dbc.Col([card_paris, html.P(), card_faq], lg=4),
#                         dbc.Col(
#                             [
#                                 main_compare,
#                                 html.P(),
#                                 card_table_budgets,
#                                 html.P(),
#                             ],
#                             lg=8,
#                         ),
#                     ]
#                 ),
#                 dcc.Interval(
#                     id="interval-component",
#                     interval=1 * 1000,  # in milliseconds
#                     n_intervals=0,
#                 ),
#             ],
#             fluid=True,
#         ),
#         html.P(),
#         html.Footer(card_about),
#     ]
# )

from components.container.container_details_budget import (
    create_container_details_budget,
)

container_details_budget = create_container_details_budget(app)


app.layout = container_details_budget


if __name__ == "__main__":
    app.run_server()
