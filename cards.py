import numpy as np
import pandas as pd
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_html_components import H4
from figures import fig_emissions_measured_vs_target, fig_target_diff_year
from custom_components import collapse_button, led
from data.compute_budget import get_remaining_paris_budget
from data.read_data import read_bisko_budget
from scenarios import cumulated_emissions, when_budget_is_spend, when_scenario_0


link_ifeu18 = html.A(
    '"CO2-Bilanzierung bis 2018 für die Stadt Heidelberg"',
    href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents_E2103137505/heidelberg/Objektdatenbank/31/PDF/01_Ifeu_Studie_CO2_Bilanzierung_bis_2018_fuer_die_Stadt_Heidelberg.pdf",
)


def card_main_compare(app, df):

    link_ifeu_homepage = html.A(
        "Institut für Energie und Umweltforschung Heidelberg (ifeu)",
        href="https://www.ifeu.de/",
    )

    link_statistisches_jb19 = html.A(
        "Statistischen Jahrbuch 2019",
        href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents_E-216793268/heidelberg/Objektdatenbank/12/PDF/Statistik/12_pdf_7.Umwelt.pdf",
    )

    link_masterplan = html.A(
        "Masterplan 100% Klimaschutz",
        href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents/heidelberg/Objektdatenbank/31/PDF/Energie%20und%20Klimaschutz/31_pdf_Masterplan%20Bericht%20und%20Ma%C3%9Fnahmen.pdf",
    )

    link_ob_suedd_19 = html.A(
        "sueddeutsche.de",
        href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents/heidelberg/Objektdatenbank/31/PDF/Energie%20und%20Klimaschutz/31_pdf_Masterplan%20Bericht%20und%20Ma%C3%9Fnahmen.pdf",
    )

    link_ob_hd_19 = html.A(
        "heidelberg.de",
        href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents/heidelberg/Objektdatenbank/31/PDF/Energie%20und%20Klimaschutz/31_pdf_Masterplan%20Bericht%20und%20Ma%C3%9Fnahmen.pdf",
    )

    link_ob_hd24_19 = html.A(
        "heidelberg24.de",
        href="https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents/heidelberg/Objektdatenbank/31/PDF/Energie%20und%20Klimaschutz/31_pdf_Masterplan%20Bericht%20und%20Ma%C3%9Fnahmen.pdf",
    )

    link_ob_rnz_19 = html.A(
        "rnz.de",
        href="https://www.rnz.de/nachrichten/heidelberg_artikel,-heidelberg-wuerzner-will-bis-2030-die-klimaneutrale-stadt-_arid,474402.html",
    )

    details_data = [
        html.H5("Zu den Daten"),
        html.P(
            [
                "Die Rohdaten, die im Balkendiagramm verwendet werden, stammen aus der ",
                link_ifeu18,
                ", die vom ",
                link_ifeu_homepage,
                " erstellt wurden. Für eine vollständige Bilanzierung des CO2-Ausstoßes der Stadt Heidelberg kann nicht auf die Daten im Heidelberger ",
                link_statistisches_jb19,
                " zurückgegriffen werden. Diese decken nur Emissionen aus energetischer Nutzung fossiler Energieträger, also insgesamt weniger als die Hälfte der Gesamtemissionen, ab. Die vorhandenen Daten liegen bis zum Jahr 2018 für volle Kalenderjahre vor, mit Ausnahme der Kategorie Verkehr. Für diese Kategorie gibt es nur Daten für 2010 und 2017, für die übrigen Jahre sind Schätzwerte dargestellt. Diese sind durch lineare Interpolation zwischen den vorhandenen Datenpunkten und konstantem Fortscheiben der Werte für das Jahr 2018 entstanden.",
            ]
        ),
    ]

    details_targets = [
        html.H5("Zu den Zielen"),
        html.H6("Warum Linear?"),
        html.P(
            [
                "Die Zielszenarien sind als (mindestens) lineare Pfade abgebildet. Das ist aus zwei Gründen wichtig: Erstens macht die Definition eines Zielpfades ein Monitoring möglich. Zweitens unterscheiden sich die Maßnahmen, die man zur Zielerreichung umsetzen muss, in ihren Kosten. Es gibt leicht umsetzbare Maßnahmen und welche, die mit denen größere Kosten einher gehen. Diese leicht umsetzbaren Maßnahmen werden vorrausichtlich zu Beginn umgesetzt. Wenn es in einer frühen Phase, in der noch kostengünstige Maßnahmen umsetzbar sind, nicht gelingt eine entsprechend große Reduzierung der Emissionen zu erreichen, dann wird eine Umsetzung der ohnehin teuren Maßnahmen gegen Ende des Reduktionszeitraums noch schwieriger.",
            ]
        ),
        html.H6("Warum gibt es zwei Ziele und warum ausgerechnet 2030 und 2050?"),
        html.P(
            [
                "Der Heidelberger Gemeinderat hat 2014 den ",
                link_masterplan,
                " verabschiedet. Darin wurde eine Reduktion der CO2-Emissionen um 95% bis zum Jahr 2050 beschlossen. Später hat der Oberbürgermeister das politische Ziel geäußert bis 2030 klimaneutral sein zu wollen (e.g. auf ",
                link_ob_suedd_19,
                ", ",
                link_ob_hd_19,
                ", ",
                link_ob_hd24_19,
                " und ",
                link_ob_rnz_19,
                "). Es kann bei diesen Äusserungen leicht der Endruck entstehen dass sich das Heidleberger Klimaziel von 2050 auf 2030 verschoben hat. Das ist aber nicht der Fall. Bei allen bisherigen Meldungen um das neue Datum 2030 handelt es sich um Denkanstöße und Wünsche. Es ist wichtig Visionen zu haben doch es ist auch wichtig die Fakten zu kennen: Heidelberg hält bisher an 2050 als verbindliches Ziel für Klimaneutralität fest.",
            ]
        ),
        html.H6("Was hat es mit den Updates der Zielpfade auf sich?"),
        html.P(
            [
                'Die Stadt Heidelberg hat seit dem Beschluss des Gemeinderates zum Masterplan 100% Klimaschutz jedes Jahr die durch einen linearen Pfad gegebenen Zwischenziele verfehlt. Wenn wir die Zieldaten weiterhin auf einem linearen Pfad erreichen wollen müssen wir ab 2018 den Updates der Zielpfade, also "Ziel 2030 Update" beziehungsweise "Ziel 2050 Update" folgen.'
            ]
        ),
    ]

    app, cbutton_maincompare = collapse_button(
        app,
        "Weitere Infos",
        dbc.CardBody(details_data + details_targets),
    )

    g_emissions_vs_target = dcc.Graph(
        id="g_emissions_vs_target",
        figure=fig_emissions_measured_vs_target(df),
    )

    card_main_compare = dbc.Card(
        dbc.CardBody(
            [
                g_emissions_vs_target,
                html.P(
                    "In diesem Diagram werden die tatsächlich gemessenen CO2-Emissionen der Stadt Heidelberg dargestellt, sowie mögliche Pfade zur Klimaneutralität  im Jahr 2030 bzw. 2050."
                ),
                cbutton_maincompare,
            ]
        )
    )
    return app, card_main_compare


def card_paris(app, df):

    link_umweltrat_budget_de = html.A(
        "Deutsche Umweltrat",
        href="https://www.umweltrat.de/SharedDocs/Downloads/EN/01_Environmental_Reports/2020_08_environmental_report_chapter_02.pdf?__blob=publicationFile&v=5",
    )
    link_newclimateorg_de = html.A(
        "newclimate.org",
        href="https://newclimate.org/wp-content/uploads/2020/05/Zwei_neue_Klimaschutzziele_f%C3%BCr_Deutschland_5_2020.pdf",
    )

    # https://www.umweltrat.de/SharedDocs/Downloads/EN/01_Environmental_Reports/2020_08_environmental_report_chapter_02.pdf?__blob=publicationFile&v=5
    @app.callback(
        Output("led_budget", "children"),
        Input("interval-component", "n_intervals"),
    )
    def led_budget(n):
        remaining_budget_kt, when_budget_is_depleted = get_remaining_paris_budget(df)
        remaining_budget_t = remaining_budget_kt * 1000
        remaining_budget_t_str = "{:.2f}".format(remaining_budget_t)
        return led(remaining_budget_t_str)

    @app.callback(
        Output("led_endyear", "children"),
        Input("interval-component", "n_intervals"),
    )
    def led_budget(n):
        remaining_budget_kt, when_budget_is_depleted = get_remaining_paris_budget(df)
        return led(when_budget_is_depleted.year)

    details = [
        html.H5("Das CO2-Budget der Stadt Heidelberg"),
        html.P(
            [
                "Im Abkommen von Paris hat sich die Weltgemeinschaft darauf verständigt Anstrengungen zu unternehmen um die globale Klimaerwärmung auf 1,5 Grad Celsius zu beschränken. Jedes Land muss seinen Beitrag leisten, damit wir dieses Ziel erreiche können. Den genauen Beitrag eines Landes zu bestimmen ist allerdings nicht einfach. Inwieweit spielen z.B. historische Emissionen eine Rolle bei der Verteilung der Lasten? ",
                link_newclimateorg_de,
                " hat sich dieser schwierigen Aufgabe angenommen und ist zu dem Ergebnis gekommen, dass Deutschland ab dem Jahr 2018 noch ein Budget von 4,6 Gigatonnen hat, um mit einer Wahrscheinlichkeit von 66% unter dem 1.5 Grad Ziel zu bleiben. Angenommen dieses Budget wird innerhalb Deutschlands gleichmäßig auf die Bevölkerung verteilt, bedeutet das ein CO2-Budget von 8932 kt für die Stadt Heidelberg.",
            ]
        ),
        html.H5("Heidelbergs Emissionen in dieser Sekunde?"),
        html.P(
            [
                "Die Emissionen der Stadt Heidelberg liegen öffentlich nur für jedes Kalenderjahr bis 2018 vor (",
                link_ifeu18,
                "). Das bedeutet, dass die Emissionen pro Sekunde nur schätzen können. Dies geschieht in ein linearen Trend aus den Jahren 2014 und den letzten bekannten Wert, also 2018, geschätzen und  auf die Sekunde runter gerechnet wird. Dase Angabe ist natürlich nicht exakt, gibt aber eine Idee zu den Größenordnungen.",
            ]
        ),
        html.H5("Bis wann ist unser Budget aufgebraucht"),
        html.P(
            [
                "Kennt man das Budget und nimmt man die oben beschriebene Rate der CO2-Emissionen an, dann lässt sich das Jahr bestimmen in dem die Stadt Heidelberg ihr CO2-Budget aufgebraucht hat. Dies ist ein Szenario in dem wir unsere Bemühungen nicht erhöhen, welches hoffentlich so nicht ein tritt.",
            ]
        ),
    ]
    app, cbutton_paris = collapse_button(app, "Weitere Infos", dbc.CardBody(details))

    card_paris = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Verbleibendes CO2-Budget für Heidelberg in Tonnen:",
                ),
                html.Div(id="led_budget"),
                html.P(),
                html.H5(
                    f"CO2-Budget aufgebraucht bis:",
                    className="card-text",
                ),
                html.Div(id="led_endyear"),
                html.P(),
                html.P(
                    "Näherungsweise Angaben des CO2-Budgets für die Stadt Heidelberg basierend auf dem Pariser Klimaabkommen",
                    className="card-title",
                ),
                cbutton_paris,
            ]
        )
    )
    return app, card_paris


def card_diff_year(app, df_compare_with_target):

    g_compare_abs = dcc.Graph(
        id="gcomp_abs_year", figure=fig_target_diff_year(df_compare_with_target)
    )

    details = (
        html.P(
            "Die beiden Graphen zeigen die Entwicklung der jährlichen Differenz (in Kilotonnen) zwischen den gemessenen Emissionen und den linearen Zielpfade zur Klimaneutralität im Jahr 2030 bzw. 2050. Die CO2-Emissionen der Stadt Heidelberg weichen Jahr für Jahr immer stärker von den Zielpfaden ab. Würden die tatsächlichen Emissionen die Zielvorgaben erreichen wäre der entsprechnede Graph hier immer auf Null. Würde ein Ziel uebererfüllt dann wäre der entsprechende Graph negativ."
        ),
    )
    app, cbutton_diff = collapse_button(app, "Weitere Infos", dbc.CardBody(details))

    card_diff_year = dbc.Card(dbc.CardBody([g_compare_abs, cbutton_diff]))

    return card_diff_year


def card_about():

    link_klimaentscheidhd = html.A(
        "Klimaentscheid Heidelberg",
        href="ttp://klimaentscheid-heidelberg.de",
    )
    link_github = html.A(
        "github",
        href="https://github.com/minorchange/co2_monitor_hd",
    )
    link_contactmail = html.A(
        "info@klimaentscheid-heidelberg.de",
        href="mailto: info@klimaentscheid-heidelberg.de",
    )

    card_imprint = dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    [
                        "Dieses Dashboard wude vom ",
                        link_klimaentscheidhd,
                        " erstellt.",
                        "Der Quellcode ist frei verfügbar und kann  auf ",
                        link_github,
                        " eingesehen werden.",
                        " Bei Fragen und Anregungen wenden Sie sich bitte an: ",
                        link_contactmail,
                    ],
                ),
            ]
        )
    )

    return card_imprint


def card_table(app, df):

    budget_start_year, bisko_budget_start_value_kt = read_bisko_budget()

    df_t = pd.DataFrame()

    df_t[" "] = [
        "Gesammte Emissionen [kt]",
        "Prozent des Pariser Budgets",
        "Paris Budget aufgebraucht",
        "Erstes Jahr 0 Emissionen",
    ]

    for scenario_name, nice_name in [
        ["scenario_target30_kt", "Ziel 2030"],
        ["scenario_target50_kt", "Ziel 2050"],
        ["scenario_target30_new_kt", f"Ziel 2030 U."],
        ["scenario_target50_new_kt", f"Ziel 2050 U."],
        ["scenario_trendlin_kt", "Trend"],
    ]:

        projected_emissions_kt = cumulated_emissions(
            df, scenario_name, from_y=budget_start_year
        )
        percentage_budget = 100 * (projected_emissions_kt / bisko_budget_start_value_kt)

        year0 = when_scenario_0(df, scenario_name)

        year_budget_depleted = when_budget_is_spend(
            df, scenario_name, bisko_budget_start_value_kt, from_y=budget_start_year
        )

        c = [
            projected_emissions_kt,
            percentage_budget,
            year_budget_depleted,
            year0,
        ]
        units = [" kt", " %", "", ""]
        c = [f"{x:.0f}{units[i]}" for i, x in enumerate(c)]

        c = [" " if x == "nan" else x for x in c]

        df_t[nice_name] = c

    table = dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df_t.columns],
        data=df_t.to_dict("records"),
    )

    details_table = [
        html.P(
            f'Hier werden die verschienenen Szenarien zur Klimaneutralität in Heidelberg verglichen. Da das Pariser Budget ab Beginn des Jahres {budget_start_year} gerechnet wird werden die entsprechenden Szenarien auch ab diesem Jahr berücksichtigt. Die "Gesammten Emissionen [kt]" etwa beziehen sich auf den Zeitraum von Anfang {budget_start_year} bis Zum Zeitpunkt, an dem die Klimaneutralität ereicht ist. Zusaetzlich wird dargestellt wieviel Prozent des ursprünglich angesetzten Pariser Budgets letztlich aufgebraucht wird und wann das Budget (also wann 100%) überschritten ist. Die letzte Zeile zeigt das Jahr an, in dem Klimaneutralität erreicht wird.'
        ),
        html.P(
            "Die Ziele 2030 und 2050 sind mittlerweile so nicht mehr realisierbar. Sie geben also an wie die Entwicklung hätte sein können, wenn Heidelberg die Ziele jedes Jahr erreicht hätte. Um sich ein Bild von den noch zu erreichenden Zielen zu machen muss man sich die beiden Updates der Zielpfade anschauen: Ziel 2030 U. und Ziel 2050 U."
        ),
    ]

    app, cbutton_table = collapse_button(
        app,
        "Weitere Infos",
        dbc.CardBody(details_table),
    )

    card_table = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Szenarien im Hinblick auf das Heidelberger CO2 Budget"),
                html.P(),
                table,
                html.P(),
                cbutton_table,
            ]
        )
    )

    return card_table
