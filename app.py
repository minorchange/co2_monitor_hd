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
from read_data import read_emissions
from budget import get_remaining_budget
from datetime import datetime
import dash_daq as daq

app = dash.Dash(
    title="hd co2 monitor",
    update_title=None,
    external_stylesheets=[dbc.themes.FLATLY],
)

df_emissions = read_emissions()

# fig_sectors = px.bar(df_emissions, x=df_emissions.index, y=df_emissions.columns)
# g_sectors = dcc.Graph(figure=fig_sectors)


def create_14_target(target_year, df_all):
    assert target_year > 2014
    assert target_year < 3000
    assert 2014 in df_all.index

    df_14_30 = pd.DataFrame({"year": range(2014, target_year + 1)})
    df_14_30["target"] = np.nan
    df_14_30 = df_14_30.set_index("year")
    val_at_startdate = df_all.sum(axis=1)[2014]
    df_14_30.loc[2014, "target"] = val_at_startdate
    df_14_30.loc[target_year, "target"] = 0
    df_14_30 = df_14_30.interpolate()
    df_res = df_14_30[df_14_30.index >= df_all.index.min()]
    # df_res = df_res[df_res.index <= df_all.index.max()]

    return df_res


t30 = create_14_target(2030, df_emissions)
t50 = create_14_target(2050, df_emissions)


# df_iris = px.data.iris() # iris is a pandas DataFrame

fig_t30 = px.line(t30, x=t30.index, y=t30.columns)
fig_t50 = px.line(t50, x=t50.index, y=t50.columns)
# g1 = dcc.Graph(figure=fig)


traces_bar = [
    go.Bar(x=df_emissions.index, y=df_emissions[c], name=c)
    for c in df_emissions.columns
]
trace_t30 = go.Scatter(x=t30.index, y=t30["target"], name="Ziel 2030", mode="lines")
trace_t50 = go.Line(x=t50.index, y=t50["target"], name="Ziel 2050", mode="lines")

f_tog = go.Figure(
    data=traces_bar + [trace_t30] + [trace_t50],
    layout=go.Layout(
        barmode="stack",
        title="Tatsaechliche CO2-Emissionen und Heidelbergs Klimaschutzziele ",
        # modebar={"orientation": "v"},
        # margin={"t": 0},
        xaxis=dict(range=[2009.5, 2030.5]),
    ),
)
g_together = dcc.Graph(id="gtogether", figure=f_tog)


df_compare_with_target = pd.DataFrame(df_emissions.sum(axis=1))
df_compare_with_target = df_compare_with_target.join(t30, how="inner").join(
    t50, how="inner", rsuffix="_"
)
df_compare_with_target.columns = ["actual_emissions", "target_2030", "target_2050"]

df_compare_with_target["diff30"] = (
    df_compare_with_target["actual_emissions"] - df_compare_with_target["target_2030"]
)
df_compare_with_target["diff50"] = (
    df_compare_with_target["actual_emissions"] - df_compare_with_target["target_2050"]
)

traces_compare_abs = [
    go.Scatter(
        x=df_compare_with_target.index,
        y=df_compare_with_target[c],
        mode="lines+markers",
    )
    for c in ["diff30", "diff50"]
]  # ['actual_emissions', 'target_2030', 'target_2050']]

f_compare_abs = go.Figure(
    data=traces_compare_abs,
    #   layout=go.Layout(xaxis=df_compare_with_target.index.to_list())
)
g_compare_abs = dcc.Graph(id="gcomp_abs", figure=f_compare_abs)


trace1 = go.Bar(x=["giraffes", "orangutans", "monkeys"], y=[20, 14, 23], name="SF Zoo")

trace2 = go.Bar(x=["giraffes", "orangutans", "monkeys"], y=[12, 18, 29], name="LA Zoo")
g2 = dcc.Graph(
    id="bar_plot",
    figure=go.Figure(data=[trace1, trace2], layout=go.Layout(barmode="stack")),
)


total_emissions_kt, when_budget_is_depleted = get_remaining_budget(df_emissions)


@app.callback(
    Output("live-update-paris-budget", "children"),
    Input("interval-component", "n_intervals"),
)
def update_paris_budget(n):

    remaining_budget_kt, when_budget_is_depleted = get_remaining_budget(df_emissions)
    remaining_budget_t = remaining_budget_kt * 1000
    remaining_budget_t_str = "{:.2f}".format(remaining_budget_t)
    g_md = dbc.CardBody(
        [
            html.H4(
                "Der Beitrag von Heidelberg zur Einhaltung des Pariser Klimaabkommens",
                className="card-title",
            ),
            html.Hr(),
            html.H6(
                f"Verbleibendes CO2-Budget fuer Heidelberg in Tonnen:",
            ),
            daq.LEDDisplay(value=remaining_budget_t_str, color="#FF5E5E"),
            html.Hr(),
            html.H6(
                f"CO2-Budget aufgebraucht bis:",
                className="card-text",
            ),
            daq.LEDDisplay(value=when_budget_is_depleted.year, color="#FF5E5E"),
            html.Hr(),
            html.P(
                f"Erklaerung",
            ),
        ]
    )

    return g_md


darker_grey = "#c2c8d0"
light_grey = "#e5ecf6"


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
                                g_together,
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
