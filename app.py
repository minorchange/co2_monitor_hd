import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash
import os
from colors import *

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


from cards import (
    header,
    card_main_compare,
    card_paris,
    card_diff_year,
    card_faq,
    card_about,
    card_table_compare_plans,
    card_table_budgets,
)

app, main_compare = card_main_compare(app, co2d)
app, card_paris = card_paris(app, co2d)
card_diff_year = card_diff_year(app, co2d)
card_faq = card_faq(app, co2d)
card_about = card_about()
card_table_compare_plans = card_table_compare_plans(app, co2d)
app, card_table_budgets = card_table_budgets(app, co2d)


app.layout = html.Div(
    [
        header,
        dbc.Container(
            [
                html.P(),
                dbc.Row(
                    [
                        dbc.Col([card_paris, html.P(), card_faq], lg=4),
                        dbc.Col(
                            [
                                main_compare,
                                html.P(),
                                card_table_budgets,
                                html.P(),
                            ],
                            lg=8,
                        ),
                    ]
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=1 * 1000,  # in milliseconds
                    n_intervals=0,
                ),
            ],
            fluid=True,
        ),
        html.P(),
        html.Footer(card_about),
    ]
)


if __name__ == "__main__":
    app.run_server()
