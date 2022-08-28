import uuid
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
from colors import *


def collapse_button(app, button_text, cardbody_collapse):

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


def set_value_buttons(app, id, options):

    button_id = id
    output_id = f"{id}_value"

    @app.callback(Output(output_id, "children"), [Input(button_id, "value")])
    def display_value(value):
        return f"Selected value: {value}"

    starting_option = options[0]["value"]
    button_group = html.Div(
        [
            dbc.RadioItems(
                id=button_id,
                # className="btn-group",
                # inputClassName="btn-check",
                # labelClassName="btn btn-outline-primary",
                # labelCheckedClassName="active",
                options=options,
                value=starting_option,
                inline=True,
            ),
            html.Div(id=output_id),
        ],
        className="radio-group",
    )

    return app, button_group


def set_value_buttons(app, id, options):

    button_id = id
    output_id = f"{id}_value"

    # @app.callback(Output(output_id, "children"), [Input(button_id, "value")])
    # def display_value(value):
    #     return f"Selected value: {value}"

    from dash import dcc

    button_group = dcc.RadioItems(
        ["New York City", "Montreal", "San Francisco"], value="Montreal", inline=True
    )
    # starting_option = options[0]["value"]
    # button_group = html.Div(
    #     [
    #         dbc.RadioItems(
    #             id=button_id,
    #             # className="btn-group",
    #             # inputClassName="btn-check",
    #             # labelClassName="btn btn-outline-primary",
    #             # labelCheckedClassName="active",
    #             options=options,
    #             value=starting_option,
    #             inline=True,
    #         ),
    #         html.Div(id=output_id),
    #     ],
    #     className="radio-group",
    # )

    return app, button_group


# def set_global_property_button(app, button_text, property, value):

#     myuuid = uuid.uuid4()
#     button_id = f"button_{myuuid}"
#     collapse_id = f"collapse_{myuuid}"

#     @app.callback(
#         Output(collapse_id, "is_open"),
#         [Input(button_id, "n_clicks")],
#         [State(collapse_id, "is_open")],
#     )
#     def toggle_collapse(n, is_open):
#         if n:
#             return not is_open
#         return is_open

#     div = html.Div(
#         [
#             dbc.Button(
#                 button_text,
#                 id=button_id,
#                 color="secondary",
#             ),
#         ]
#     )
#     return app, div


# def collapse_button(app, button_text, cardbody_collapse, button_same_hight_text=""):

#     myuuid = uuid.uuid4()
#     button_id = f"button_{myuuid}"
#     collapse_id = f"collapse_{myuuid}"

#     @app.callback(
#         Output(collapse_id, "is_open"),
#         [Input(button_id, "n_clicks")],
#         [State(collapse_id, "is_open")],
#     )
#     def toggle_collapse(n, is_open):
#         if n:
#             return not is_open
#         return is_open

#     div = html.Div(
#         [
#             dbc.Row(
#                 [
#                     dbc.Button(
#                         button_text,
#                         id=button_id,
#                         color="secondary",
#                     ),
#                     html.P("BLUBB", style={"text-align": "center"}),
#                 ]
#             ),
#             dbc.Collapse(dbc.Card(cardbody_collapse), id=collapse_id, is_open=False),
#         ]
#     )
#     return app, div


def led(nstr):

    led = daq.LEDDisplay(value=nstr, color=trend_color, size=30)
    return led
