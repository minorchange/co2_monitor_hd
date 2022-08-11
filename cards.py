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

link_ifeu20 = html.A(
    '"Klimaschutzziele und Maßnahmen - Controlling für die Stadt Heidelberg"',
    href="http://gemeinderat.heidelberg.de/getfile.asp?id=338418&type=do",
)

link_bisko = html.A(
    "BISKO-Systematik",
    href="https://www.kea-bw.de/fileadmin/user_upload/Energiemanagement/Angebote/Beschreibung_der_BISKO-Methodik.pdf",
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
        href="https://www.sueddeutsche.de/politik/klimaschutz-heidelberg-klimanotstand-1.4720018",
    )

    link_ob_hd24_19 = html.A(
        "heidelberg24.de",
        href="https://www.heidelberg24.de/heidelberg/heidelberg-klimaneutral-2030-diesen-massnahmen-solls-klappen-13142437.html",
    )

    link_ob_rnz_19 = html.A(
        "rnz.de",
        href="https://www.rnz.de/nachrichten/heidelberg_artikel,-heidelberg-wuerzner-will-bis-2030-die-klimaneutrale-stadt-_arid,474402.html",
    )

    details_data = [
        html.H5("Zu den Daten"),
        html.P(
            [
                "Die Rohdaten, die im Balkendiagramm verwendet werden, stammen aus den Berichten ",
                link_ifeu18,
                " und ",
                link_ifeu20,
                ", die vom ",
                link_ifeu_homepage,
                " nach der ",
                link_bisko,
                " erstellt wurden. Für eine vollständige Bilanzierung des CO2-Ausstoßes der Stadt Heidelberg kann nicht auf die Daten im Heidelberger ",
                link_statistisches_jb19,
                " zurückgegriffen werden. Diese decken nur Emissionen aus energetischer Nutzung fossiler Energieträger, also insgesamt weniger als die Hälfte der Gesamtemissionen, ab. Die vorhandenen Daten liegen bis zum Jahr 2020 für volle Kalenderjahre vor, mit Ausnahme der Kategorie Verkehr. Für diese Kategorie wurden in den Jahren 2011 bis 2014 keine Daten erhoben. Hier bedienen wir uns Schätzwerten. Diese sind durch lineare Interpolation zwischen den vorhandenen Datenpunkten entstanden. Da die Daten nach der ",
                link_bisko,
                " erstellt wurden umfassen sie nur Emissionen, die innerhalb der Grenzen der Kommune emittiert werden. Laut Kapitel 2.3 in ",
                link_ifeu18,
                " umfassen sie Damit explizit nicht alle, von Heidelberger Bürgern verursachten Emissionen.",
            ]
        ),
        html.H5("Die Jahre 2019 und 2020"),
        html.P(
            [
                "Bei der Veröffentlichung der Emissionen in den Jahren nach 2018 in ",
                link_ifeu20,
                " ist es den Autor*innen wichtig die aktuellen Zahlen wie folgt einzuordnen: ",
            ],
        ),
        html.P(
            [
                '"Die Jahre 2019 und 2020 zeigen eine stark fallende Tendenz der CO 2 - Emissionen. Tatsächlich werden im Bereich der Gebäudewärme seit vielen Jahren deutliche Einsparungen erzielt. Vor allem liegen die hohen Einsparungen an einem starken Ausbau der Erneuerbaren Energien in Deutschland, was die spezifischen Emissionen des bundesdeutschen Strommixes deutlich sinken ließ. Im Jahr 2020 kommen noch „Corona-Effekte“ vor allem im Verkehrsbereich hinzu, insgesamt lagen die Fahrleistungen deutlich geringer als in den Vorjahren, was sich auch in der Heidelberger CO 2 -Bilanz niederschlägt. Es wird ausdrücklich davor gewarnt, eine lineare Fortsetzung dieser Entwicklung zu erwarten. Genaues Zahlenmaterial für die CO 2 -Bilanz 2021 liegt zwar noch nicht vor, Tendenzen der Bundesentwicklung deuten aber darauf hin, dass sowohl der CO 2 -Emissionsfaktor für den Strom wieder ansteigt („Windschwaches Jahr 2021“ 10), als auch der Verkehrsbereich wieder an das Niveau von 2019 anschließt."',
            ],
        ),
        html.P(
            [
                "Dieser Einordnung schlißen wir uns an. Es ist vor diesem Hintergrund wichtig den dargestellten Trend nicht als Prognose zu verstehen. Vielmehr soll er, ähnlich der Zielpfade ein mögliches Szenario durchspielen."
            ],
        ),
        html.P(
            [
                "Zudem Weisen die Autor*innen darauf hin, dass die Emissionswerte für das Jahr 2020 noch vorläufig sind."
            ],
        ),
    ]

    details_targets = [
        html.H5("Zu den Zielen"),
        html.P(
            [
                "Die Zielpfade sind, wie auch die Emissionswerte dem Bericht ",
                link_ifeu20,
                " entnommen.",
            ]
        ),
        # html.H6("Warum gibt es zwei Ziele und warum ausgerechnet 2030 und 2050?"),
        # html.P(
        #     [
        #         "Der Heidelberger Gemeinderat hat 2014 den ",
        #         link_masterplan,
        #         ' verabschiedet. Darin wurde eine Reduktion der CO2-Emissionen um 95% bis zum Jahr 2050 beschlossen. Später hat der Oberbürgermeister das politische Ziel geäußert bis 2030 klimaneutral sein zu wollen. Z.B.: "Der Gemeinderat hat nun beschlossen, bis 2030 klimaneutral zu sein." [',
        #         link_ob_suedd_19,
        #         '], "Wir sollten uns das Ziel setzen, dass Heidelberg bis zum Jahr 2030 eine klimaneutrale Stadt wird. ..." [',
        #         link_ob_hd24_19,
        #         '] und "Wir müssen alles dafür tun, dass Heidelberg bis 2030 klimaneutral ist" [',
        #         link_ob_rnz_19,
        #         "]. Es kann bei diesen Äußerungen leicht der Endruck entstehen dass sich das Heidelberger Klimaziel von 2050 auf 2030 verschoben hat. Das ist aber nicht der Fall. Bei allen bisherigen Meldungen um das neue Datum 2030 handelt es sich um Denkanstöße und Wünsche. Es ist wichtig Visionen zu haben doch es ist auch wichtig die Fakten zu kennen: Heidelberg hält bisher an 2050 als verbindliches Ziel für Klimaneutralität fest.",
        #     ]
        # ),
        html.H6("Was hat es mit den Updates der Zielpfade auf sich?"),
        html.P(
            [
                'Die Stadt Heidelberg hat seit dem Beschluss des Gemeinderates zum Masterplan 100% Klimaschutz jedes Jahr die durch einen linearen Pfad gegebenen Zwischenziele verfehlt. Wenn wir die Zieldaten weiterhin auf einem linearen Pfad erreichen wollen müssen wir ab 2018 den Updates der Zielpfade, also "EU Mission 2030 Update" beziehungsweise "Szenario 2040 Update" folgen.'
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
                    [
                        "In diesem Diagram werden die tatsächlich gemessenen CO2-Emissionen der Stadt Heidelberg nach der ",
                        link_bisko,
                        " dargestellt. Zudem sind mögliche Pfade zur Klimaneutralität im Jahr 2030 und 2040, sowie der aktuelle Trend abgebildet.",
                    ],
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
    link_parisagreement = html.A(
        "Abkommen von Paris",
        href="https://de.wikipedia.org/wiki/%C3%9Cbereinkommen_von_Paris",
    )
    link_statista2015hdnrpersons = html.A(
        "statista.com",
        href="https://de.statista.com/statistik/daten/studie/375849/umfrage/entwicklung-der-gesamtbevoelkerung-in-heidelberg/",
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
        # wbid = when_budget_is_depleted
        led_content = f"{wbid.day} . {wbid.month} . {wbid.year}"

        return led(led_content)

    details = [
        html.H5("Das CO2-Budget der Stadt Heidelberg"),
        html.P(
            [
                "Im völkerrechtlich bindenden ",
                link_parisagreement,
                " hat sich die Weltgemeinschaft darauf verständigt Anstrengungen zu unternehmen um die globale Klimaerwärmung auf 1,5 Grad Celsius zu beschränken. Jedes Land muss seinen Beitrag leisten, damit wir dieses Ziel erreiche können. Den genauen Beitrag eines Landes zu bestimmen ist allerdings nicht einfach. Inwieweit spielen z.B. historische Emissionen eine Rolle bei der Verteilung der Lasten? ",
                link_newclimateorg_de,
                " hat sich dieser schwierigen Aufgabe angenommen und ist zu dem Ergebnis gekommen, dass Deutschland ab dem Jahr 2018 noch ein CO2 Budget von 4,6 Gigatonnen hat um mit einer Wahrscheinlichkeit von 66% die Pariser Klimaziele zu erreichen. Teilen wir das deutsche Budget gleichmäßig auf die Bevölkerung auf dann hat die Stadt Heidelberg ab 2018 ein CO2 Budget von 8932 kt zur Verfügung.",
            ]
        ),
        html.H5("Das BISKO Budget"),
        html.H5("Allgemein"),
        html.P(
            [
                "Das oben beschriebene Heidelberger Budget umfasst sowohl Emissionen, die innerhalb der Grenzen des der Kommune emittiert werden (Verkehr, private Haushalte, Gewerbe, Industrie, ...), als auch von Heidelbergern verursachte Emissionen außerhalb des Stadtgebiets (Konsumgüter. Investitionsgüter, Fahrzeuge, Baumaterialien, ...). Laut Kapitel 2.3 in der ",
                link_ifeu18,
                " erfasst Heidelberg nach der ",
                link_bisko,
                " nur die erstgenannten, also nur die Emissionen die im Territorium Heidelbergs entstehen. Um dem Rechnung zu tragen müssen wir das Heidelberger Budget von 8932 kt differenziert betrachten. Ein Teil des Budgets kann für BISKO-Emissionen aufgewendet werden. Der Rest ist den Nicht-BISKO Emissionen vorbehalten.",
            ]
        ),
        html.H5("Berechnung"),
        html.P(
            [
                "Wie genau wollen wir aber nun diese Aufteilung des Gesamtbudgets vornehmen? In Kapitel 2.3 in ",
                link_ifeu18,
                " werden für das Jahr 2015 jeder Heidelberger Bürger:in durchschnittliche Emissionen von 11,2 Tonnen CO2 bescheinigt. Da wir von ",
                link_statista2015hdnrpersons,
                " die Einwohnerzahl Heidelbergs in 2015 ermitteln können: 156267, Können wir leicht die Gesamten Emissionen für 2015 berechnen: 1750.19 kt. Aus der Balkengrafik aus diesem Dashboard lesen wir einen Wert für die BISKO-Emissionen von 1117.43 kt ab. Das bedeutet dass wir nur rund 64% der Gesamtemissionen Heidelbergs durch die BISKO-Emissionen erfassen. Folgerichtig sollte unser BISKO-Budget auch nur rund 64% der Gesamtbudgets betragen. Wir gehen also von rund (1117.43 kt / 1750.19 kt) * 8932 kt = 5703 kt als BISKO-Budget aus. Dies ist das Budget, dass wir für die in der ",
                link_ifeu18,
                " erfassten Emissionen haben. Auf dieser Basis wird das Verbleibende Restbudget und das Jahr, bis zu dem wir, bei fortschreitendem Trend, das Budget aufgebraucht haben werden.",
            ]
        ),
        html.H5("Heidelbergs Emissionen in dieser Sekunde?"),
        html.P(
            [
                "Die Emissionen der Stadt Heidelberg liegen öffentlich nur für die Kalenderjahre bis einschließlich 2020 vor (",
                link_ifeu18,
                " und ",
                link_ifeu20,
                "). Das bedeutet, dass die Emissionen pro Sekunde nur schätzen können. Dies geschieht in ein linearen Trend aus den Jahren 2014 und den letzten bekannten Wert, also 2020, geschätzten und  auf die Sekunde runter gerechnet wird. Diese Angabe ist natürlich nicht exakt, gibt aber eine Idee zu den Größenordnungen.",
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
                    "Näherungsweise Angaben des CO2-Budgets für die Stadt Heidelberg basierend auf dem Pariser Klimaabkommen und der Annahme, dass sich der Trend der Emissionen in Heidelberg unverändert fortsetzt.",
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
            "Die beiden Graphen zeigen die Entwicklung der jährlichen Differenz (in Kilotonnen) zwischen den gemessenen Emissionen und den linearen Zielpfade zur Klimaneutralität im Jahr 2030 bzw. 2040. Die CO2-Emissionen der Stadt Heidelberg weichen, bis zum Jahr 2018 immer stärker von den Zielpfaden ab. Danach sehen wir eine Annäherung an beide Zielpfade. Wir notieren allerdings weiterhin eine Untererfüllung der Ziele. Würden die tatsächlichen Emissionen die Zielvorgaben immer erreichen wäre der entsprechende Graph hier immer auf Null. Da es sich mit der Klimaerwärmung um ein kumulatives Problem handelt ist ein Erreichen der Nullline nicht mehr genug. Um vergangene Versäumnisse zu kompensieren müssen wir unsere Ziele in Zukunft übererfüllen. Im Falle einer Übererfüllung sähen wir negative Werte."
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
                        "Dieses Dashboard wurde vom ",
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
        "Gesamte Emissionen [kt]",
        "Prozent des Pariser Budgets",
        "Paris Budget aufgebraucht",
        "Erstes Jahr 0 Emissionen",
    ]

    for scenario_name, nice_name in [
        ["scenario_target30_kt", "EU Mission 2030"],
        ["scenario_target40_kt", "Szenario 2040"],
        ["scenario_target30_new_kt", f"EU Mission 2030 U."],
        ["scenario_target40_new_kt", f"Szenario 2040 U."],
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
            f'Hier werden die verschiedenen Szenarien zur Klimaneutralität in Heidelberg verglichen. Da das Pariser Budget ab Beginn des Jahres {budget_start_year} gerechnet wird werden die entsprechenden Szenarien auch ab diesem Jahr berücksichtigt. Die "Gesamten Emissionen [kt]" etwa beziehen sich auf den Zeitraum von Anfang {budget_start_year} bis Zum Zeitpunkt, an dem die Klimaneutralität erreicht ist. Zusätzlich wird dargestellt wieviel Prozent des ursprünglich angesetzten Pariser Budgets letztlich aufgebraucht wird und wann das Budget (also wann 100%) überschritten ist. Die letzte Zeile zeigt das Jahr an, in dem Klimaneutralität erreicht wird.'
        ),
        html.P(
            "Die Ziele 2030 und 2040 sind mittlerweile so nicht mehr realisierbar. Sie geben also an wie die Entwicklung hätte sein können, wenn Heidelberg die Ziele jedes Jahr erreicht hätte. Um sich ein Bild von den noch zu erreichenden Zielen zu machen muss man sich die beiden Updates der Zielpfade anschauen: EU Mission 2030 U. und Szenario 2040 U."
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
