import os

proj_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(proj_dir)


import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import dash_core_components as dcc
import plotly.express as px
from data.read_data import read_emissions
from data.create_target import create_target_line, compare_emissions_with_target
from data.compute_budget import get_remaining_budget
from create_figures import fig_emissions_measured_vs_target, fig_target_diff
from callbacks import _update_paris_budget
from datetime import datetime
import dash_daq as daq


# data
df_emissions = read_emissions()
df_t30 = create_target_line(2014, 2030, df_emissions)
df_t50 = create_target_line(2014, 2050, df_emissions)
df_compare_with_target = compare_emissions_with_target(df_emissions, df_t30, df_t50)
total_emissions_kt, when_budget_is_depleted = get_remaining_budget(df_emissions)


# graphs
g_emissions_vs_target = dcc.Graph(
    id="g_emissions_vs_target",
    figure=fig_emissions_measured_vs_target(df_emissions, df_t30, df_t50),
)

g_compare_abs = dcc.Graph(
    id="gcomp_abs", figure=fig_target_diff(df_compare_with_target)
)


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
    return _update_paris_budget(df_emissions)


app.layout = dbc.Container(
    [
        dbc.NavbarSimple(brand="CO2-Monitor Heidelberg", fluid=True),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(id="live-update-paris-budget"),
                    md=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Klimaziele der Stadt Heidelberg"),
                                g_emissions_vs_target,
                                g_compare_abs,
                            ]
                        )
                    ),
                    md=8,
                ),
            ]
        ),
        dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        ),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server()
