import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

from datetime import datetime

app = dash.Dash()


app.layout = html.Div(
    html.Div(
        [
            html.Div(id="live-update-text"),
            dcc.Interval(
                id="interval-component",
                interval=1 * 1000,  # in milliseconds
                n_intervals=0,
            ),
            dcc.Tabs(
                id="tabs",
                value="tab-1",
                children=[
                    dcc.Tab(label="Global Budget", value="tab-1"),
                    dcc.Tab(label="Total Budget HD", value="tab-2"),
                ],
            ),
            html.Div(id="tabs-content"),
        ]
    )
)


@app.callback(
    Output("tabs-content", "children"),
    [Input("interval-component", "n_intervals"), Input("tabs", "value")],
)
def update_time(n, tab):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # return [html.Span(current_time)]

    if tab == "tab-1":
        return html.Div(html.Span(current_time))
    elif tab == "tab-2":
        return html.Div("Blubb")


if __name__ == "__main__":
    app.run_server(debug=True)
