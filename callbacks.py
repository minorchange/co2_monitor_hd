import dash_html_components as html
import dash_daq as daq
from data.compute_budget import get_remaining_paris_budget
import dash_bootstrap_components as dbc


def _update_paris_budget(df):

    remaining_budget_kt, when_budget_is_depleted = get_remaining_paris_budget(df)
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
            daq.LEDDisplay(value=remaining_budget_t_str, color="#FF5E5E", size=30),
            html.Hr(),
            html.H6(
                f"CO2-Budget aufgebraucht bis:",
                className="card-text",
            ),
            daq.LEDDisplay(
                value=when_budget_is_depleted.year, color="#FF5E5E", size=30
            ),
            html.Hr(),
            html.P(
                f"Erklaerung",
            ),
            dbc.Button(
                "Open collapse",
                id="collapse-button",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                id="collapse",
            ),
        ]
    )

    return g_md