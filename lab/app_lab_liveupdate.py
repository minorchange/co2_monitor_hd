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
        ]
    )
)


@app.callback(
    Output("live-update-text", "children"), Input("interval-component", "n_intervals")
)
def update_time(n):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return [html.Span(current_time)]


if __name__ == "__main__":
    app.run_server(debug=True)
