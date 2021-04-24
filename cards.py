import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from figures import fig_emissions_measured_vs_target, fig_target_diff
from custom_components import collapse_button, led
from data.compute_budget import get_remaining_budget


def card_main_compare(app, df_emissions, df_t30, df_t50):

    app, cbutton_maincompare = collapse_button(
        app, "Mehr Info", dbc.CardBody("blubb blubb")
    )

    g_emissions_vs_target = dcc.Graph(
        id="g_emissions_vs_target",
        figure=fig_emissions_measured_vs_target(df_emissions, df_t30, df_t50),
    )
    card_main_compare = dbc.Card(
        dbc.CardBody(
            [
                html.H4("Klimaziele der Stadt Heidelberg"),
                g_emissions_vs_target,
                cbutton_maincompare,
            ]
        )
    )
    return app, card_main_compare


def card_paris(app, df_emissions):
    @app.callback(
        Output("led_budget", "children"),
        Input("interval-component", "n_intervals"),
    )
    def led_budget(n):
        remaining_budget_kt, when_budget_is_depleted = get_remaining_budget(
            df_emissions
        )
        remaining_budget_t = remaining_budget_kt * 1000
        remaining_budget_t_str = "{:.2f}".format(remaining_budget_t)
        return led(remaining_budget_t_str)

    @app.callback(
        Output("led_endyear", "children"),
        Input("interval-component", "n_intervals"),
    )
    def led_budget(n):
        remaining_budget_kt, when_budget_is_depleted = get_remaining_budget(
            df_emissions
        )
        return led(when_budget_is_depleted.year)

    app, cbutton_paris = collapse_button(
        app, "Mehr Info", dbc.CardBody("This content is hidden in the ")
    )

    card_paris = dbc.Card(
        dbc.CardBody(
            [
                html.H4(
                    "Der Beitrag von Heidelberg zur Einhaltung des Pariser Klimaabkommens",
                    className="card-title",
                ),
                html.Hr(),
                html.H6(
                    f"Verbleibendes CO2-Budget fuer Heidelberg in Tonnen:",
                ),
                dbc.Card(id="led_budget"),
                # daq.LEDDisplay(value=remaining_budget_t_str, color="#FF5E5E", size=30),
                html.Hr(),
                html.H6(
                    f"CO2-Budget aufgebraucht bis:",
                    className="card-text",
                ),
                dbc.Card(id="led_endyear"),
                html.Hr(),
                # daq.LEDDisplay(value=when_budget_is_depleted.year, color="#FF5E5E", size=30)
                cbutton_paris,
                # dbc.Button(
                #     "Open collapse",
                #     id="collapse-button",
                #     block=True,
                #     color="info",
                # ),
                # dbc.Collapse(
                #     dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                #     id="collapse",
                # ),
            ]
        )
    )
    return app, card_paris