import dash
from dash import dcc
from dash import html
import uuid


def create_tabcomponent(app, list_of_titlecontenttuples, start_tuple_id=0):

    assert start_tuple_id < len(list_of_titlecontenttuples)

    random_id = str(uuid.uuid4())[:8]
    tab_id = f"tabs-{random_id}"
    tab_content_id = f"{tab_id}-content"

    children_list = [
        dcc.Tab(label=tup[0], value=tab_id + f"-{i}")
        for i, tup in enumerate(list_of_titlecontenttuples)
    ]

    tabcomponent = html.Div(
        [
            dcc.Tabs(
                id=tab_id,
                value=tab_id + f"-{start_tuple_id}",
                children=children_list,
            ),
            html.Div(id=tab_content_id),
        ]
    )

    @app.callback(
        dash.dependencies.Output(tab_content_id, "children"),
        [dash.dependencies.Input(tab_id, "value")],
    )
    def render_content(tab):
        this_tab_id = int(tab.split("-")[-1])
        return list_of_titlecontenttuples[this_tab_id][1]

    return app, tabcomponent


if __name__ == "__main__":

    app = dash.Dash(__name__)

    l = [("Tab1", "Das ist das Haus vom Nikolauis"), ("Blubbname", html.H1("GAGAGAG"))]
    app, tabcomponent = create_tabcomponent(app, l, start_tuple_id=1)

    app.layout = html.Div(
        [
            tabcomponent,
        ]
    )

    app.run_server(debug=True)
