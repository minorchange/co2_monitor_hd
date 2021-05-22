import plotly.graph_objs as go
from colors import *


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
            marker_color=barcolors[i],
        )
        for i, c in enumerate(individual_measurements_colnames)
    ]

    s_e = df["co2_kt_total"]
    trace_e_sum = go.Scatter(
        x=s_e.index,
        y=s_e.values,
        name="Gesammtemissionen",
        mode="lines+markers",
        line=dict(color="grey", width=2),
        visible="legendonly",
    )

    trace_target30 = go.Scatter(
        x=df.index,
        y=df["target30_kt"],
        name="Ziel 2030",
        mode="lines",
        line=dict(color=target_30_color, width=2),
    )

    trace_target50 = go.Scatter(
        x=df.index,
        y=df["target50_kt"],
        name="Ziel 2050",
        mode="lines",
        line=dict(color=target_50_color, width=2),
    )

    trace_target30_new = go.Scatter(
        x=df.index,
        y=df["target30_new_kt"],
        name="Ziel 2030 - Update",
        mode="lines",
        line=dict(color=target_30_color, dash="dash", width=2),
        visible="legendonly",
    )

    trace_target50_new = go.Scatter(
        x=df.index,
        y=df["target50_new_kt"],
        name="Ziel 2050 - Update",
        mode="lines",
        line=dict(color=target_50_color, dash="dash", width=2),
        visible="legendonly",
    )

    trace_trend = go.Scatter(
        x=df.index,
        y=df["trend_lin_kt"],
        name="Trend",
        mode="lines",
        line=dict(color=trend_color, width=2),  # dash="dot",
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
            title="CO2-Emissionen der Stadt Heidelberg und gesteckte Ziele zur Klimaneutralität.",
            title_font_family="Open Sans",
            title_font_color="#212529",
            title_font_size=16,
            xaxis=dict(range=[2009.5, 2030.5]),
            template=template,
            xaxis_title="Jahr",
            yaxis_title="CO2 Emissionen [kt]",
        ),
    )

    return f_emissions_m_v_t


def fig_target_diff_year(df):

    nicenames = ["Diff. zum Ziel 2030", "Diff. zum Ziel 2050"]
    colors = [target_30_color, target_50_color]
    traces_compare_abs = [
        go.Scatter(
            x=df[df[c].isna() == False].index,
            y=df[c][df[c].isna() == False],
            mode="lines+markers",
            name=nicenames[i],
            line=dict(color=colors[i], width=3),
            # color=[target_30_color, target_50_color],
        )
        for i, c in enumerate(["diff_target30_kt", "diff_target50_kt"])
    ]

    f_compare_abs = go.Figure(
        data=traces_compare_abs,
        layout=go.Layout(
            # title="Differenz der CO2-Emissionen zu den Zielenpfaden<br>Klimaneutralität 2030 bzw. 2050",
            title="Mehremmisionen",
            xaxis=dict(range=[2013.5, 2018.5]),
            title_font_family="Open Sans",
            title_font_color="#212529",
            title_font_size=16,
            legend=dict(yanchor="top", y=0.97, xanchor="left", x=0.03),
            template=template,
            xaxis_title="Jahr",
            yaxis_title="CO2 Mehremissionen [kt]",
        ),
    )

    return f_compare_abs
