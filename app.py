import uuid
from dash_bootstrap_components._components import CardColumns
from dash_bootstrap_components._components.Card import Card
from dash_bootstrap_components._components.Col import Col
import dash_daq as daq
from datetime import datetime
from callbacks import _update_paris_budget
from figures import fig_emissions_measured_vs_target, fig_target_diff_year
from data.compute_budget import get_remaining_paris_budget
from data.target import (
    create_target_line,
    compare_emissions_with_target,
    add_targets,
)
from trend import add_trend, add_trend_continuation
from data.read_data import read_emissions
from custom_components import collapse_button
import plotly.express as px
import numpy as np


import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash
import os

proj_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(proj_dir)


# data
df_emissions = read_emissions()
df = df_emissions
df["co2_kt_total"] = df.sum(axis=1)

df = add_trend(df)
df = add_trend_continuation(df)
df = add_targets(df)

# (
#     df_compare_with_target,
#     df_t30,
#     df_t50,
#     new_lin_target_30,
#     new_lin_target_50,
#     df_t30_new,
#     df_t50_new,
# ) = compute_new_line_targets(df_emissions)


# total_emissions_kt, when_paris_budget_is_depleted = get_remaining_paris_budget(
# df_emissions, trend
# )


# app
title_for_tab = "hd co2 monitor"
app = dash.Dash(
    title=title_for_tab,
    update_title=None,
    external_stylesheets=[dbc.themes.FLATLY],
)


@app.callback(
    Output("live-update-paris-budget", "children"),
    Input("interval-component", "n_intervals"),
)
def update_paris_budget(n):
    return _update_paris_budget(df)


header = dbc.NavbarSimple(brand="CO2-Monitor Heidelberg", fluid=True)


from cards import (
    card_main_compare,
    card_paris,
    card_audit_year,
    card_audit_cumulated,
    card_imprint,
)

app, main_compare = card_main_compare(app, df)
app, card_paris = card_paris(app, df)
card_audit_year = card_audit_year(df)
card_audit_cumulated = card_audit_cumulated(df)
card_imprint = card_imprint()


app.layout = dbc.Container(
    [
        header,
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([card_paris, html.P(), card_imprint], md=4),
                # , style={"min-width": "400px"}),
                dbc.Col(
                    [
                        main_compare,
                        html.P(),
                        dbc.CardDeck([card_audit_year, card_audit_cumulated]),
                    ],
                    md=8,
                ),
            ]
        ),
        dcc.Interval(
            id="interval-component",
            interval=1 * 1000,
            n_intervals=0,  # in milliseconds
        ),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server()
