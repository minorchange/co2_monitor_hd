from callbacks import _update_paris_budget
from data.target import add_targets
from trend import add_trend
from scenarios import (
    add_scenarios,
    when_scenario_0,
    cumulated_emissions,
    cumulated_emissions_this_second,
    when_budget_is_spend,
)
from data.read_data import read_emissions
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash
import os
from colors import *


proj_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(proj_dir)


# data
df_emissions = read_emissions()
df = df_emissions
df["co2_kt_total"] = df.sum(axis=1)

df = add_trend(df)
df = add_targets(df)

df = add_scenarios(df)

when_scenario_0(df, "scenario_trendconst_kt")
cumulated_emissions(df, "scenario_trendlin_kt", from_y=2014, to_y=2022)
cumulated_emissions_this_second(df, "scenario_trendlin_kt", from_y=2017)
when_budget_is_spend(df, "scenario_trendlin_kt", 6000, from_y=2017)


# app
title_for_tab = "hd co2 monitor"
app = dash.Dash(
    title=title_for_tab,
    update_title=None,
    external_stylesheets=[dbc.themes.SIMPLEX],
)


@app.callback(
    Output("live-update-paris-budget", "children"),
    Input("interval-component", "n_intervals"),
)
def update_paris_budget(n):
    return _update_paris_budget(df)


header = dbc.Navbar(
    html.A(
        dbc.Row(
            [
                dbc.Col(html.Img(src="/assets/klimaentscheid-logo.jpg", height="45px")),
                dbc.Col(
                    dbc.NavbarBrand(
                        "CO2-Monitor Heidelberg",
                        className="ml-2",
                        # style={"color": "red", "font-weight": "bold"},
                    )
                ),
            ],
            align="center",
        ),
        href="https://klimaentscheid-heidelberg.de",
        className="g-0",  # no gutters
    ),
    sticky="top",
    color="white",
    style={"border-width": "0px", "box-shadow": "0 6px 6px -6px #999"},
)


from cards import (
    card_main_compare,
    card_paris,
    card_diff_year,
    card_about,
    card_table,
)

app, main_compare = card_main_compare(app, df)
app, card_paris = card_paris(app, df)
card_diff_year = card_diff_year(app, df)
card_about = card_about()
card_table = card_table(app, df)


app.layout = html.Div(
    [
        header,
        dbc.Container(
            [
                html.P(),
                dbc.Row(
                    [
                        dbc.Col([card_paris, html.P(),
                                  card_diff_year
                                  ], lg=4),
                        dbc.Col(
                            [
                                main_compare,
                                html.P(),
                                card_table,
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
