import uuid
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
from components.colors import *


def create_collapse_button(app, button_text, cardbody_collapse):
    myuuid = uuid.uuid4()
    button_id = f"button_{myuuid}"
    collapse_id = f"collapse_{myuuid}"

    @app.callback(
        Output(collapse_id, "is_open"),
        [Input(button_id, "n_clicks")],
        [State(collapse_id, "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    div = html.Div(
        [
            dbc.Button(
                button_text,
                id=button_id,
                color="secondary",
            ),
            dbc.Collapse(dbc.Card(cardbody_collapse), id=collapse_id, is_open=False),
        ]
    )
    return app, div
