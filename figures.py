import plotly.graph_objs as go


def fig_emissions_measured_vs_target(df):

    df_e_nicenames = [
        "Private Haushalte",
        "Industrie",
        "Gebäude Stadt",
        "Gewerbe u. Sonstige",
        "Verkehr",
    ]

    individual_measurements_colnames = [
        "co2_kt_privatehh",
        "co2_kt_industrie",
        "co2_kt_staedtgeb",
        "co2_kt_gewerbe_u_oeffentlgeb",
        "co2_kt_traffic",
    ]

    traces_bar = [
        go.Bar(
            x=df.index,
            y=df[c],
            name=df_e_nicenames[i],
        )
        for i, c in enumerate(individual_measurements_colnames)
    ]

    s_e = df["co2_kt_total"]
    trace_e_sum = go.Scatter(
        x=s_e.index,
        y=s_e.values,
        name="Gesammtemissionen",
        mode="lines+markers",
        line=dict(color="grey"),
        visible="legendonly",
    )

    trace_target30 = go.Scatter(
        x=df.index,
        y=df["target30_kt"],
        name="Ziel 2030",
        mode="lines",
        line=dict(color="cadetblue"),
    )

    trace_target50 = go.Scatter(
        x=df.index,
        y=df["target50_kt"],
        name="Ziel 2050",
        mode="lines",
        line=dict(color="crimson"),
    )

    trace_target30_new = go.Scatter(
        x=df.index,
        y=df["target30_new_kt"],
        name="Ziel 2030 - Update",
        mode="lines",
        line=dict(color="cadetblue", dash="dash"),
        visible="legendonly",
    )

    trace_target50_new = go.Scatter(
        x=df.index,
        y=df["target30_new_kt"],
        name="Ziel 2050 - Update",
        mode="lines",
        line=dict(color="crimson", dash="dash"),
        visible="legendonly",
    )

    trace_trend = go.Scatter(
        x=df.index,
        y=df["trend_lin_kt"],
        name="Trend",
        mode="lines",
        line=dict(color="red", dash="dot"),
        # visible="legendonly",
    )

    f_emissions_m_v_t = go.Figure(
        data=[trace_e_sum]
        + traces_bar
        + [
            trace_target30_new,
            trace_target30,
            trace_target50_new,
            trace_target50,
            trace_trend,
        ],
        layout=go.Layout(
            barmode="stack",
            title="Tatsaechliche CO2-Emissionen und Heidelbergs Klimaschutzziele ",
            xaxis=dict(range=[2009.5, 2030.5]),
        ),
    )

    return f_emissions_m_v_t


# def fig_emissions_measured_vs_target(
#     df_emissions, df_target30, df_target50, df_target30_new, df_target50_new, trend
# ):

#     df_e_nicenames = [
#         "Private Haushalte",
#         "Industrie",
#         "Gebäude Stadt",
#         "Gewerbe u. Sonstige",
#         "Verkehr",
#     ]
#     traces_bar = [
#         go.Bar(
#             x=df_emissions.index,
#             y=df_emissions[c],
#             name=df_e_nicenames[i],
#         )
#         for i, c in enumerate(df_emissions.columns)
#     ]

#     s_e = df_emissions.sum(axis=1)
#     trace_e_sum = go.Scatter(
#         x=s_e.index,
#         y=s_e.values,
#         name="Gesammtemissionen",
#         mode="lines+markers",
#         line=dict(color="grey"),
#         visible="legendonly",
#     )

#     trace_target30 = go.Scatter(
#         x=df_target30.index,
#         y=df_target30["target"],
#         name="Ziel 2030",
#         mode="lines",
#         line=dict(color="cadetblue"),
#     )

#     trace_target50 = go.Scatter(
#         x=df_target50.index,
#         y=df_target50["target"],
#         name="Ziel 2050",
#         mode="lines",
#         line=dict(color="crimson"),
#     )

#     trace_target30_new = go.Scatter(
#         x=df_target30_new.index,
#         y=df_target30_new["target"],
#         name="Ziel 2030 - Update",
#         mode="lines",
#         line=dict(color="cadetblue", dash="dash"),
#         visible="legendonly",
#     )

#     trace_target50_new = go.Scatter(
#         x=df_target50_new.index,
#         y=df_target50_new["target"],
#         name="Ziel 2050 - Update",
#         mode="lines",
#         line=dict(color="crimson", dash="dash"),
#         visible="legendonly",
#     )

#     trace_trend = go.Scatter(
#         x=trend.df.index,
#         y=trend.df["trend"],
#         name="Trend",
#         mode="lines",
#         line=dict(color="red", dash="dot"),
#         # visible="legendonly",
#     )

#     f_emissions_m_v_t = go.Figure(
#         data=[trace_e_sum]
#         + traces_bar
#         + [
#             trace_target30_new,
#             trace_target30,
#             trace_target50_new,
#             trace_target50,
#             trace_trend,
#         ],
#         layout=go.Layout(
#             barmode="stack",
#             title="Tatsaechliche CO2-Emissionen und Heidelbergs Klimaschutzziele ",
#             xaxis=dict(range=[2009.5, 2030.5]),
#         ),
#     )

#     return f_emissions_m_v_t


def fig_target_diff_year(df):

    traces_compare_abs = [
        go.Scatter(
            x=df.index,
            y=df[c],
            mode="lines+markers",
        )
        for c in ["diff_target30_kt", "diff_target50_kt"]
    ]

    f_compare_abs = go.Figure(
        data=traces_compare_abs,
    )

    return f_compare_abs


def fig_target_diff_cumulated(df):

    traces_compare_abs = [
        go.Scatter(
            x=df.index,
            y=df[c].cumsum(),
            mode="lines+markers",
        )
        for c in ["diff_target30_kt", "diff_target50_kt"]
    ]

    f_compare_abs = go.Figure(
        data=traces_compare_abs,
    )

    return f_compare_abs
