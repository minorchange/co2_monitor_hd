import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from data.data import co2d
from components.cards import (
    # header,
    create_card_main_compare,
    create_card_paris,
    create_card_faq,
    card_imprint,
    # create_card_table_compare_plans,
    create_card_table_budgets,
)


def create_container_details_budget(app):
    # title_for_tab = "CO₂ Monitor Heidelberg"
    # app = dash.Dash(
    #     title=title_for_tab,
    #     update_title=None,
    #     external_stylesheets=[dbc.themes.SIMPLEX],
    # )

    app, main_compare = create_card_main_compare(app, co2d)
    app, card_paris = create_card_paris(app, co2d)
    card_faq = create_card_faq(app, co2d)
    app, card_table_budgets = create_card_table_budgets(app, co2d)

    container = html.Div(
        [
            # header,
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
            html.Footer(
                card_imprint(),
                # style={
                #     "text-align": "center",
                # },
            ),
        ]
    )

    return app, container
