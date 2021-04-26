import plotly.graph_objs as go


def fig_emissions_measured_vs_target(
    df_emissions, df_t30, df_t50, df_t30_new, df_t50_new
):

    df_e_nicenames = [
        "Private Haushalte",
        "Industrie",
        "Gebäude Stadt",
        "Gewerbe u. Sonstige",
        "Verkehr",
    ]
    traces_bar = [
        go.Bar(
            x=df_emissions.index,
            y=df_emissions[c],
            name=df_e_nicenames[i],
        )
        for i, c in enumerate(df_emissions.columns)
    ]

    # trace_t30 = go.Scatter(
    #     x=df_t30.index, y=df_t30["target"], name="Ziel 2030", mode="lines"
    # )
    trace_t30 = go.Scatter(
        x=df_t30.index,
        y=df_t30["target"],
        name="Ziel 2030",
        mode="lines",
        line=dict(color="cadetblue"),
    )

    # trace_t50 = go.Line(
    #     x=df_t50.index, y=df_t50["target"], name="Ziel 2050", mode="lines"
    # )

    trace_t50 = go.Scatter(
        x=df_t50.index,
        y=df_t50["target"],
        name="Ziel 2050",
        mode="lines",
        line=dict(color="crimson"),
    )

    trace_t30_new = go.Scatter(
        x=df_t30_new.index,
        y=df_t30_new["target"],
        name="Ziel 2030 - Update",
        mode="lines",
        line=dict(color="cadetblue", dash="dash"),
    )

    trace_t50_new = go.Scatter(
        x=df_t50_new.index,
        y=df_t50_new["target"],
        name="Ziel 2050 - Update",
        mode="lines",
        line=dict(color="crimson", dash="dash"),
    )

    f_emissions_m_v_t = go.Figure(
        data=traces_bar + [trace_t30_new, trace_t50_new, trace_t30, trace_t50],
        layout=go.Layout(
            barmode="stack",
            title="Tatsaechliche CO2-Emissionen und Heidelbergs Klimaschutzziele ",
            xaxis=dict(range=[2009.5, 2030.5]),
        ),
    )

    return f_emissions_m_v_t


def fig_target_diff_year(df_compare_with_target):

    traces_compare_abs = [
        go.Scatter(
            x=df_compare_with_target.index,
            y=df_compare_with_target[c],
            mode="lines+markers",
        )
        for c in ["diff30", "diff50"]
    ]

    f_compare_abs = go.Figure(
        data=traces_compare_abs,
    )

    return f_compare_abs


def fig_target_diff_cumulated(df_compare_with_target):

    traces_compare_abs = [
        go.Scatter(
            x=df_compare_with_target.index,
            y=df_compare_with_target[c],
            mode="lines+markers",
        )
        for c in ["diff30cumsum", "diff50cumsum"]
    ]

    f_compare_abs = go.Figure(
        data=traces_compare_abs,
    )

    return f_compare_abs
