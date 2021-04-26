import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_html_components import H4
from figures import (
    fig_emissions_measured_vs_target,
    fig_target_diff_cumulated,
    fig_target_diff_year,
    fig_target_diff_cumulated,
)
from custom_components import collapse_button, led
from data.compute_budget import get_remaining_paris_budget


link_ifeu18 = html.A(
    '"CO2-Bilanzierung bis 2018 für die Stadt Heidelberg"',
    href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents_E2103137505/heidelberg/Objektdatenbank/31/PDF/01_Ifeu_Studie_CO2_Bilanzierung_bis_2018_fuer_die_Stadt_Heidelberg.pdf",
)


def card_main_compare(app, df_emissions, df_t30, df_t50, df_t30_new, df_t50_new):

    link_ifeu_homepage = html.A(
        "Institut für Energie und Umweltforschung Heidelberg (ifeu)",
        href="https://www.ifeu.de/",
    )

    link_statistisches_jb19 = html.A(
        "Statistischen Jahrbuch 2019",
        href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents_E-216793268/heidelberg/Objektdatenbank/12/PDF/Statistik/12_pdf_7.Umwelt.pdf",
    )

    details_data = [
        html.H5("Zu den Daten"),
        html.P(
            [
                "Die Rohdaten, die im Balkendiagramm verwendet werden stammen aus der ",
                link_ifeu18,
                ", die vom ",
                link_ifeu_homepage,
                " erstellt wurde. Man beachte dass man für eine vollständige Bilanzierung des heidelberger CO2 Ausstoßes nicht auf die Daten im Heidelberger ",
                link_statistisches_jb19,
                " zurückgreifen kann. Diese decken nur Emissionen aus energetischer Nutzung fossiler Energieträger, also insgesamt weniger als die Hälfte der Gesamtemmisionen, ab. Die vorhandenen Daten liegen bisher nur bis zum Jahr 2018 vor. Bis auf den Verkehr liegen sie für volle Kalenderjahre vor. Für den Verkehr gab es in jüngerer Vergangenheit nur in den beiden Jahren 2010 und 2017 Daten. Die oben dargestellten Daten für den Verkehr sind also teilweise Schätzwerte. Diese sind durch lineare Interpretation zwischen den vorhandenen Werten und konstantem fortscheiben der Werte für das Jahr 2018 entstanden.",
            ]
        ),
    ]

    details_targets = [
        html.H5("Zu den Zielen"),
        html.H6("Warum Linear?"),
        html.P(
            [
                "Die Zielszenarien sind allesamt (mindestens) lineare Pfade. Das ist aus 2 Gründen wichtig: Erstens macht ein Pfad im Vergleich zu einem reinen Zieldatum ein Monitoring möglich. Zweitens unterscheiden sich die Maßnahmen, die man zur Zielerreichung umsetzen muss, in ihren Kosten. Es gibt leicht umsetzbare Maßnahmen und welche, mit denen größere Kosten einher gehen. Diese leicht umsetzbaren sollten natürlich zu Beginn umgesetzt werden. Wenn es uns in einer frühen Phase, in der noch günstige Maßnahemen umsetzbar sind, nicht gelingt eine entsprechend große Reduzierung der Emissionen zu erreichen dann wird eine Umsetzung der ohnehin teuren Maßnahmen gegen Ende des Reduktionszeitraums noch schwieriger.",
            ]
        ),
        html.H6("Warum gibt es 2 Ziele und warum gerade 2030 und 2050?"),
        html.P(
            [
                'Der Heidelberger Gemeinderat hat 2014 den "Masterplan 100% Klimaschutz" verabschiedet [Quelle?]. Darin wurde eine Reduktion der CO2 Emissionen um 95% bis zum Jahr 2050 beschlossen. Später hat der Oberbürgermeister das politische Ziel geäußert bis 2030 klimaneutral sein zu wollen [Quellen?]. Es ist an dieser Stelle aber wichtig festzuhalten dass das verbindliche Ziel der Stadt Heidelberg immer noch 2050 ist und bisher nicht auf 2030 geändert wurde.',
            ]
        ),
    ]

    details_targetsupdate = [
        html.H5("Zu den Updates der Ziele"),
        html.P(
            [
                "Heidelberg hat seit dem Beschluss des Gemeinderates zum Masterplan 100% Klimaschutz jedes Jahr die durch einen linearen Pfad gegebenen Zwischenziele verfehlt. Selbst wenn wir ab 2019 jedes Jahr exakt den Zwischenzielen der linearen Pfade entsprächen haben wir im Jahr 2030 bzw. 2050 insgesamt mehr emittiert als der Lineare Pfad vorgesehen hätte. Um ein Gefühl dafür zu bekommen wie viel Emissionsschulden wir mittlerweile angehäuft haben sind 2 geupdatete Ziele in der Grafik mit dargestellt. Diese Weisen eine Linearen Pfad von 2018 an, der in Summe über die Komplette Laufzeit des Plans genau so viel CO2 Emissionen verursacht, wie die ursprünglichen Pläne. Man beachte dass man in solch einem Szenario die Zielzeitpunkte von 2030 auf 2025 und von 2050 auf 2044 verschieben müsste. Wir haben also grob gesprochen in den 5 Jahren von 2014 bis 2018 soweit über das Ziel hinausgeschossen dass wir das Zieljahr um  mindestens 5 Jahre nach vorne verschieben müssen damit unsere gesamten Emissionen im Reduktionszeitraum denen entsprechen, die von den ursprünglichen Zielen Vorgegeben sind.",
            ]
        ),
    ]

    app, cbutton_maincompare = collapse_button(
        app,
        "Mehr Infos",
        dbc.CardBody(details_data + details_targets + details_targetsupdate),
    )

    g_emissions_vs_target = dcc.Graph(
        id="g_emissions_vs_target",
        figure=fig_emissions_measured_vs_target(
            df_emissions, df_t30, df_t50, df_t30_new, df_t50_new
        ),
    )
    card_main_compare = dbc.Card(
        dbc.CardBody(
            [
                g_emissions_vs_target,
                html.P(
                    "Hier werden die tatsächlich gemessenen CO2 Emissionen den gesteckten Zielen gegenübergestellt. Zusätzlich werden neue 2 neue Zielpfade eingeführt die den bisherigen Emissionen Rechnung tragen. Sie skizzieren Szenarien, in denen im Zeitraum von 2014 bis zum jeweiligen Zieljahr für Klimaneutralität genau so viel CO2 emittiert wird wie in einer Welt, in der der entsprechenden Zielpfad realisiert wäre."
                ),
                cbutton_maincompare,
            ]
        )
    )
    return app, card_main_compare


def card_paris(app, df_emissions):

    link_umweltrat_budget_de = html.A(
        "Deutsche Umweltrat",
        href="https://www.umweltrat.de/SharedDocs/Downloads/EN/01_Environmental_Reports/2020_08_environmental_report_chapter_02.pdf?__blob=publicationFile&v=5",
    )

    #     link_umweltrat_budget_de =
    # https://www.umweltrat.de/SharedDocs/Downloads/EN/01_Environmental_Reports/2020_08_environmental_report_chapter_02.pdf?__blob=publicationFile&v=5
    @app.callback(
        Output("led_budget", "children"),
        Input("interval-component", "n_intervals"),
    )
    def led_budget(n):
        remaining_budget_kt, when_budget_is_depleted = get_remaining_paris_budget(
            df_emissions
        )
        remaining_budget_t = remaining_budget_kt * 1000
        remaining_budget_t_str = "{:.2f}".format(remaining_budget_t)
        return led(remaining_budget_t_str)

    @app.callback(
        Output("led_endyear", "children"),
        Input("interval-component", "n_intervals"),
    )
    def led_budget(n):
        remaining_budget_kt, when_budget_is_depleted = get_remaining_paris_budget(
            df_emissions
        )
        return led(when_budget_is_depleted.year)

    details = [
        html.H5("Heidelbergs CO2 Budget"),
        html.P(
            [
                "Im Abkommen von Paris hat sich die Weltgemeinschaft darauf verständigt die Globale Erwärmung hoffentlich auf 1.5, auf jeden Fall aber auf 2 Grad Celsius zu limitieren. Jedes Land muss seinen Beitrag leisten, damit wir dieses Ziel erreiche können. Den genauen Beitrag eines Landes zu bestimmen ist allerdings nicht einfach. Inwieweit spielen e.g. historische Emissionen eine Rolle bei der verteilung der Lasten? Der ",
                link_umweltrat_budget_de,
                " hat sich dieser schwierigen Aufgabe angenommen und ist zu dem Ergebnis gekommen, dass Deutschland ab dem Jahr 2020 noch ein Budget von 6.7 Gigatonnen hat. Will man die Lasten innerhalb Deutschlands gleichmache auf die Bevoelkerung aufteilen dann kommt Heidelberg auf ein Budget von 13009 kt.",
            ]
        ),
        html.H5("Heidelbergs Emissionen in dieser Sekunde?"),
        html.P(
            [
                "Die Heidelberger Emissionen liegen leider nur pro Kalenderjahr und nur bis 2018 vor (",
                link_ifeu18,
                "). Das bedeutet dass wir die Emissionen pro Sekunde nur schätzen können. Dies geschieht einfach in dem wir den letzten uns bekannten Wert, also von 2018, nehmen und diesen auf die Sekunde runter rechnen. Das ist natürlich nicht exakt, gibt aber eine Idee von den Größenordnungen.",
            ]
        ),
        html.H5("Bis wann ist unser Budget aufgebraucht"),
        html.P(
            [
                "Kennt man das Budget und nimmt man die oben beschriebene Rate der CO2 Emissionen dann lässt sich das Jahr bestimmen in dem wir unser Budget aufgebraucht haben. Dies ist das Szenario wenn wir nichts an unseren Emissionen ändern und tritt so hoffentlich nicht ein.",
            ]
        ),
    ]
    app, cbutton_paris = collapse_button(app, "Mehr Infos", dbc.CardBody(details))

    card_paris = dbc.Card(
        dbc.CardBody(
            [
                html.H4(
                    "Der Beitrag von Heidelberg zur Einhaltung des Pariser Klimaabkommens",
                    className="card-title",
                ),
                html.Hr(),
                html.H6(
                    f"Verbleibendes CO2-Budget fuer Heidelberg in Tonnen:",
                ),
                dbc.Card(id="led_budget"),
                html.Hr(),
                html.H6(
                    f"CO2-Budget aufgebraucht bis:",
                    className="card-text",
                ),
                dbc.Card(id="led_endyear"),
                html.Hr(),
                cbutton_paris,
            ]
        )
    )
    return app, card_paris


def card_audit_year(df_compare_with_target):

    g_compare_abs = dcc.Graph(
        id="gcomp_abs_year", figure=fig_target_diff_year(df_compare_with_target)
    )

    detail_compare = dbc.Card(
        dbc.CardBody(
            [
                g_compare_abs,
            ]
        )
    )

    return detail_compare


def card_audit_cumulated(df_compare_with_target):

    g_compare_abs_cum = dcc.Graph(
        id="gcomp_abs_cum", figure=fig_target_diff_cumulated(df_compare_with_target)
    )

    detail_compare_cum = dbc.Card(
        dbc.CardBody(
            [
                g_compare_abs_cum,
            ]
        )
    )

    return detail_compare_cum


# detail_compare2 = dbc.Card(
#     dbc.CardBody(
#         [
#             g_compare_abs2,
#         ],
#     )
# )


# # g_compare_abs2 = dcc.Graph(
#     id="gcomp_abs2", figure=fig_target_diff(df_compare_with_target)
# )
