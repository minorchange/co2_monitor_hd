import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from components.cards import footer


def create_container_tldr(app):

    container = html.Div(
        [
            dbc.Container(
                [
                    html.Div(
                        [
                            html.P(),
                            html.Img(
                                src="/assets/Logo_Klima_Summit_NikW.JPG", height="245px"
                            ),
                            html.P(),
                            html.H3(
                                "Heidelberg trägt dazu bei, dass Deutschland seine völkerrechtlich verbindlichen Klimaziele verfehlt."
                            ),
                            html.H4(
                                "Gegen Ende dieses Jahres wird ein Punkt erreicht, an dem selbst bei einer vollständigen Einstellung aller CO₂-Emissionen das Ziel, die globale Erwärmung auf 1,5 Grad Celsius zu begrenzen, wahrscheinlich unerreichbar sein wird. Diese Entwicklung unterstreicht die Unzulänglichkeit bisheriger Klimapolitik. Es ist absehbar, dass mit einer Wahrscheinlichkeit von über 50% auch das langfristige Ziel einer maximalen Erwärmung um 2 Grad Celsius verfehlt wird, sofern die bisherigen Klimaschutzpläne nicht signifikant ambitionierter gestaltet werden."
                            ),
                        ],
                        style={
                            "text-align": "center",
                            "display": "flex",
                            "flex-direction": "column",
                            "align-items": "center",
                            "justify-content": "center",
                        },
                    ),
                    footer,
                ],
                fluid=True,
            ),
            # html.Footer(card_about),
        ]
    )

    return app, container
