import numpy as np
import pandas as pd
from dash import dash_table, html
from dash.dependencies import Input, Output, State
from dash import dcc
import dash_bootstrap_components as dbc
from dash.html import H4
from components.figures import fig_emissions_measured_vs_plan, fig_target_diff_year

# from components.custom_components import collapse_button, led
from components.custom_components.custom_collapse_button import create_collapse_button
from components.custom_components.custom_led import create_led
from data.compute_budget import get_remaining_paris_budget_next_deadline
from data.read_data import read_bisko_budget
from components.scenarios import (
    cumulated_emissions,
    when_budget_is_spend,
    when_budget_is_spend_plan_nicestr,
    when_scenario_0,
    cumulated_emissions_this_second_plan,
)


# header = dbc.Navbar(
#     html.A(
#         dbc.NavbarBrand(
#             "CO₂-Monitor Heidelberg",
#             className="mx-auto",  # Centering the text horizontally
#             # style={
#             #     "position": "absolute",
#             #     "left": "50%",
#             #     "transform": "translateX(-50%)",
#             # },  # Centering the text absolutely
#         ),
#         style={
#             "position": "absolute",
#             "left": "50%",
#             "transform": "translateX(-50%)",
#             "zIndex": "1",
#         },  # Adding positioning styles directly to html.A
#         className="g-0",  # no gutters
#         # dbc.NavbarBrand(
#         #     "CO₂-Monitor Heidelberg",
#         #     className="text-center w-100",
#         # ),
#         # className="g-0",  # no gutters
#     ),
#     sticky="top",
#     color="white",
#     style={"border-width": "0px", "box-shadow": "0 6px 6px -6px #999"},
# )

header = dbc.Navbar(
    html.A(
        dbc.Row(
            [
                dbc.Col(
                    html.Img(src="/assets/klimaentscheid-logo.jpg", height="45px"),
                ),
                dbc.Col(
                    html.Img(src="assets/yx2.jpg", height="45px"),
                ),
                dbc.Col(
                    dbc.NavbarBrand(
                        "CO₂-Monitor Heidelberg",
                        className="ml-2",
                        # style={"color": "red", "font-weight": "bold"},
                    )
                ),
            ],
            align="center",
        ),
        href="https://klimanetz-heidelberg.de/",
        className="g-0",  # no gutters
    ),
    sticky="top",
    color="white",
    style={"border-width": "0px", "box-shadow": "0 6px 6px -6px #999"},
)


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


def create_card_main_compare(app, co2d):
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
        html.H5("Zu den Messdaten"),
        html.P(
            [
                "Die Grundlage für das Balkendiagramm bilden Rohdaten aus den Berichten ",
                link_ifeu18,
                " und ",
                link_ifeu20,
                ", erstellt vom ",
                link_ifeu_homepage,
                " nach der ",
                link_bisko,
                ". Beachten Sie, dass die Daten im Heidelberger ",
                link_statistisches_jb19,
                " nicht für eine umfassende Bilanzierung des CO₂-Ausstoßes der Stadt Heidelberg herangezogen werden konnten. Diese beschränken sich lediglich auf Emissionen aus der energetischen Nutzung fossiler Energieträger und decken somit weniger als die Hälfte der Gesamtemissionen ab. Die vorliegenden Daten reichen bis zum Jahr 2020 für volle Kalenderjahre, außer in der Kategorie Verkehr, für die in den Jahren 2011 bis 2014 keine Daten vorliegen. In diesem Fall wurden Schätzwerte durch lineare Interpolation zwischen den vorhandenen Datenpunkten erzeugt.",
            ]
        ),
    ]

    details_targets = [
        html.H5("Zum Plan"),
        html.P(
            [
                "Die geplanten Emissionen sind dem ",
                html.A(
                    "Heidelberger Klimaschutsplan",
                    href="https://app.climateview.global/v3/public/board/2ae7af89-40d4-4ff0-892c-febbfb36886f",
                ),
                " entnommen. Die veröffentlichten Pläne reichen nur bis zum Jahr 2040. Zu diesem Zeitpunkt wird die Menge der Emissionen nur auf rund 45% der Emissionsmenge im Jahr 2020 gesunken sein. Für die Betrachtung der Jahre nach 2040 haben wir den linearen trend weiter geschrieben. Das erste Jahr mit Nullemissionen ist danach 2068.",
            ]
        ),
    ]

    app, cbutton_maincompare = create_collapse_button(
        app,
        "Weitere Infos",
        dbc.CardBody(details_data + details_targets),
    )

    g_emissions_vs_target = dcc.Graph(
        id="g_emissions_vs_target",
        figure=fig_emissions_measured_vs_plan(co2d),
    )

    card_main_compare = dbc.Card(
        dbc.CardBody(
            [
                html.H5("CO₂ Bilanz und Plan"),
                g_emissions_vs_target,
                # html.P(
                #     "In diesem Diagram werden die tatsächlich gemessenen CO₂-Emissionen der Stadt Heidelberg sowie deren geplante Emissionen dargestellt."
                # ),
                cbutton_maincompare,
            ]
        )
    )
    return app, card_main_compare


def create_card_paris(app, co2d):
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
        (
            remaining_budget_kt,
            when_budget_is_depleted,
            row_index,
            col_index,
        ) = get_remaining_paris_budget_next_deadline(co2d)
        remaining_budget_t = remaining_budget_kt * 1000
        remaining_budget_t_str = "{:.2f}".format(remaining_budget_t)

        return [create_led(remaining_budget_t_str)]

    @app.callback(
        Output("led_endyear", "children"),
        Input("interval-component", "n_intervals"),
    )
    def led_year(n):
        def get_german_month_name(month_number):
            assert month_number >= 1
            assert month_number <= 12

            german_months = [
                "Januar",
                "Februar",
                "März",
                "April",
                "Mai",
                "Juni",
                "Juli",
                "August",
                "September",
                "Oktober",
                "November",
                "Dezember",
            ]
            return german_months[month_number - 1]

        (
            remaining_budget_kt,
            when_budget_is_depleted,
            row_index,
            col_index,
        ) = get_remaining_paris_budget_next_deadline(co2d)
        led_content = f"{str(when_budget_is_depleted.day).zfill(2)}.{str(when_budget_is_depleted.month).zfill(2)}.{when_budget_is_depleted.year}"

        return html.Div(
            [
                dbc.Row(
                    [
                        html.Div(
                            (create_led(str(when_budget_is_depleted.day).zfill(2)))
                        ),
                        html.Div(
                            create_led(str(when_budget_is_depleted.month).zfill(2))
                        ),
                        html.Div(create_led(str(when_budget_is_depleted.year))),
                    ],
                    style={"marginLeft": "0px"},
                ),
                html.P(),
                html.P(
                    f"Im {get_german_month_name(when_budget_is_depleted.month)} {when_budget_is_depleted.year} wird die Stadt Heidelberg voraussichtlich das ihr CO₂ Budget für die Erreichung des {row_index} Grad Zieles mit einer Wahrscheinlichkeit von {col_index.replace('p', '')}% aufgebraucht haben."
                ),
            ]
        )

        # return create_led(led_content)

    details = [
        html.H5("Das CO₂-Budget der Stadt Heidelberg"),
        html.P(
            [
                "Im völkerrechtlich bindenden ",
                link_parisagreement,
                " hat sich die Weltgemeinschaft darauf verständigt Anstrengungen zu unternehmen um die globale Klimaerwärmung auf 1,5 Grad Celsius zu beschränken. Jedes Land muss seinen Beitrag leisten, damit wir dieses Ziel erreiche können. Den genauen Beitrag eines Landes zu bestimmen ist allerdings nicht einfach. Inwieweit spielen z.B. historische Emissionen eine Rolle bei der Verteilung der Lasten? ",
                link_newclimateorg_de,
                " hat sich dieser schwierigen Aufgabe angenommen und ist zu dem Ergebnis gekommen, dass Deutschland ab dem Jahr 2018 noch ein CO₂ Budget von 4,6 Gigatonnen hat um mit einer Wahrscheinlichkeit von 66% die Pariser Klimaziele zu erreichen. Teilen wir das deutsche Budget gleichmäßig auf die Bevölkerung auf dann hat die Stadt Heidelberg ab 2018 ein CO2 Budget von 8932 kt zur Verfügung.",
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
                " werden für das Jahr 2015 jeder Heidelberger Bürger:in durchschnittliche Emissionen von 11,2 Tonnen CO₂ bescheinigt. Da wir von ",
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
                "Kennt man das Budget und nimmt man die oben beschriebene Rate der CO₂-Emissionen an, dann lässt sich das Jahr bestimmen in dem die Stadt Heidelberg ihr CO₂-Budget aufgebraucht hat. Dies ist ein Szenario in dem wir unsere Bemühungen nicht erhöhen, welches hoffentlich so nicht ein tritt.",
            ]
        ),
    ]
    # app, cbutton_paris = create_collapse_button(
    #     app, "Weitere Infos", dbc.CardBody(details)
    # )

    card_paris = dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H5(f"Nächste Budgetüberschreitung:"),
                        html.P(),
                        html.Div(id="led_endyear"),
                        html.P(),
                        html.P(
                            "Das entsprechende Restbudget in Tonnen ist hier wird hier dargestellt:"
                        ),
                        html.H5("Restbudget"),
                        html.Div(id="led_budget"),
                    ]
                ),
                html.P(),
                html.P(
                    "Die konkrete Berechnung sowie die Daten der Budgetüberschreitung für weitere Termeraturziele sind im Kästchen 'CO₂ Budgets' undtergebracht.",
                ),
                # cbutton_paris,
            ]
        )
    )
    return app, card_paris


def create_card_faq(app, co2d):
    teaser_tex = html.Div(
        [
            html.H5("Bewertbarkeit von Klimapolitik"),
            html.Div(
                [
                    html.P(
                        [
                            "Der Sachverständigenrat  für Umweltfragen beschreibt in einer ",
                            html.A(
                                "Stellungnahme",
                                href="https://www.umweltrat.de/SharedDocs/Downloads/DE/04_Stellungnahmen/2020_2024/2022_06_fragen_und_antworten_zum_co2_budget.pdf?__blob=publicationFile&v=33",
                            ),
                            " die 3 wichtigsten Kriterien, anhand derer sich nationale Klimapolitik bewerten lässt. Diese gelten natürlich auch für internationale oder kommunale Klimapolitik:",
                        ]
                    ),
                    html.P(),
                    html.H6("1. Umsetzungslücke"),
                    html.P(
                        [
                            "Eine Umsetzungslücke liegt dann vor, wenn die tatsächlichen Emissionen nicht den politisch beschlossenen Reduktionszielen entsprechen. Um frühzeitig zu erkennen ob eine Umsetzungslücke besteht bietet sich ein direkter Vergleich der Messdaten mit den ursrünglich geplanten Emissionen an. Heidelberg selbst führt einen solchen Vergleich in ihrem ",
                            html.A(
                                "Klimaschutzplan",
                                "https://app.climateview.global/v3/public/board/2ae7af89-40d4-4ff0-892c-febbfb36886f",
                            ),
                            ". Auch im Kästchen 'CO₂ Bilanz und Plan' werden wir über die nächsten Jahre genau nachverfolgen ob es in Heidelberg eine Umsetzungslücke gibt.",
                        ]
                    ),
                    html.H6("2. Ambitionslücke"),
                    html.P(
                        "Eine Ambitionslücke liegt dann vor, wenn die gesteckten Ziele der Emissionsreduktion nicht mit den völkerrechtlich verbindlichen Zielen von Paris kompatibel sind. Hier bietet sich eine Analyse an, ob und, wenn ja, wann die entsprechenden CO₂-Budgets aufgebraucht sein werden. Wie eine solche Analyse ausschauen könnte finden Sie im Kästchen 'CO₂ Budgets'."
                    ),
                    html.H6("3. Transparenzlücke"),
                    html.P(
                        "Eine Transparenzlücke liegt dann vor, wenn Umsetzungslücke und Ambitionslücke nicht quantitativ bestimmt und öffentlich kommuniziert werden. In Heidelberg wird derzeit die Umsetzungslücke, nicht aber die Ambitionslücke kommuniziert. Wir versuchen auf diesem Dashboard die fehlenden Informationen bereitzustellen und hoffen, dass die Stadt Heidelberg zeitnah selbst die Transparenzlücke schließt."
                    ),
                ]
            ),
        ]
    )

    card_faq = dbc.Card(dbc.CardBody([teaser_tex]))

    return card_faq


def create_card_diff_year(app, co2d):
    g_compare_abs = dcc.Graph(
        id="gcomp_abs_year", figure=fig_target_diff_year(co2d.df_emissions_hd)
    )

    details = (
        html.P(
            "Die beiden Graphen zeigen die Entwicklung der jährlichen Differenz (in Kilotonnen) zwischen den gemessenen Emissionen und den linearen Zielpfade zur Klimaneutralität im Jahr 2030 bzw. 2040. Die CO₂-Emissionen der Stadt Heidelberg weichen, bis zum Jahr 2018 immer stärker von den Zielpfaden ab. Danach sehen wir eine Annäherung an beide Zielpfade. Wir notieren allerdings weiterhin eine Untererfüllung der Ziele. Würden die tatsächlichen Emissionen die Zielvorgaben immer erreichen wäre der entsprechende Graph hier immer auf Null. Da es sich mit der Klimaerwärmung um ein kumulatives Problem handelt ist ein Erreichen der Nullline nicht mehr genug. Um vergangene Versäumnisse zu kompensieren müssen wir unsere Ziele in Zukunft übererfüllen. Im Falle einer Übererfüllung sähen wir negative Werte."
        ),
    )
    # app, cbutton_diff = create_collapse_button(
    #     app, "Weitere Infos", dbc.CardBody(details)
    # )

    card_diff_year = dbc.Card(dbc.CardBody([g_compare_abs, cbutton_diff]))

    return card_diff_year


def card_imprint():
    link_klimaentscheidhd = html.A(
        "Klimaentscheid Heidelberg",
        href="http://klimaentscheid-heidelberg.de",
    )
    link_klimanetz = html.A(
        "Klimanetz-Heidelberg",
        href="https://klimanetz-heidelberg.de/",
    )
    link_github = html.A(
        "github",
        href="https://github.com/minorchange/co2_monitor_hd",
    )
    link_contactmail = html.A(
        "admin@klimanetz-heidelberg.de",
        href="mailto: admin@klimanetz-heidelberg.de",
    )

    card_imprint = dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    [
                        "Dieses Dashboard wurde initial vom ",
                        link_klimaentscheidhd,
                        " erstellt und wird mittlerweile vom ",
                        link_klimanetz,
                        " betrieben und gewartet. Der Quellcode ist frei verfügbar und kann  auf ",
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


footer = html.Footer(
    card_imprint(),
    style={
        "position": "fixed",
        "bottom": 0,
        "width": "100%",
        # "background-color": "#f8f9fa",
        # "padding": "10px",
        # "text-align": "center",
    },
)

# footer = dbc.Navbar(
#     card_imprint(),
#     # sticky="bottom",
#     fixed="bottom",
#     # color="white",
#     # style={"border-width": "0px", "box-shadow": "0 -6px 6px -6px #999"},
# )


def create_card_table_compare_plans(app, co2d):
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
            co2d.df_emissions_hd, scenario_name, from_y=budget_start_year
        )
        percentage_budget = 100 * (projected_emissions_kt / bisko_budget_start_value_kt)

        year0 = when_scenario_0(co2d.df_emissions_hd, scenario_name)

        year_budget_depleted = when_budget_is_spend(
            co2d.df_emissions_hd,
            scenario_name,
            bisko_budget_start_value_kt,
            from_y=budget_start_year,
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

    # app, cbutton_table = create_collapse_button(
    #     app,
    #     "Weitere Infos",
    #     dbc.CardBody(details_table),
    # )

    card_table = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Szenarien im Hinblick auf das Heidelberger CO₂ Budget"),
                html.P(),
                table,
                html.P(),
                # cbutton_table,
            ]
        )
    )

    return card_table


def pddf2dashtable(df, id, index_col_name):
    df_dt = df.reset_index().rename(columns={"index": index_col_name})
    table = dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in df_dt.columns],
        data=df_dt.reset_index().to_dict("records"),
    )
    return table


def nice_temp_precent_table(df, id):
    df_nice = df.copy()
    index_col_name = "Ziel Temperaturerhöhung [°C]"
    df_nice.index = df_nice.index.astype(str) + "°C"
    df_nice.columns = df_nice.columns.str.replace("[^0-9]", "", regex=True) + "%"
    df_nice = df_nice.round(1)
    table = pddf2dashtable(df_nice, id, index_col_name)
    return table


def create_card_table_budgets(app, co2d):
    # Global Budget (latest numbers from ipcc)
    table_glob_latest = nice_temp_precent_table(
        co2d.df_budget_latest_global_kt.round(2).astype(str) + " kt",
        "table_budgets_global",
    )
    text_glob_latest = html.P(
        [
            "Aus einem ",
            html.A(
                "Bericht des IPCCs von 2021",
                href="https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf",
            ),
            f" (S.29) geht hervor, welche Menenge CO₂ die gesamte Menschheit ab dem Jahr {co2d.budget_latest_start_date.year} noch emittieren darf um die entsprechenden Temperaturziele (+1.5°C, +1.7°C, +2.0°C) mit einer entsprechenden Wahrscheinlichkeit (17%-83%) zu erreichen.",
        ]
    )

    text_emissions_global_from2016 = html.P(
        [
            "In Tab 3) werden wir die Globalen Emissionen zwischen 2016 und 2019 benötigen. Hier verwenden wir Daten von ",
            html.A(
                "ourworldindata.org",
                href="https://ourworldindata.org/co2-emissions",
            ),
            f".",
        ]
    )

    table_global_budget_2016 = nice_temp_precent_table(
        co2d.df_budget_2016_global_kt.round(2).astype(str) + " kt",
        "table_global_budget_2016",
    )
    text_global_budget_2016 = html.P(
        [
            'Das Pariser Klimaabkommen wurde Ende 2015 während der UN-Klimakonferenz in Paris verabschiedet. In diesem Abkommen verpflichten sich die Staaten dazu, die globale Erwärmung auf "deutlich unter" zwei Grad Celsius im Vergleich zur vorindustriellen Zeit zu begrenzen und Anstrengungen für eine Begrenzung auf 1,5 Grad Celsius zu unternehmen. Dies bildet die Grundlage dafür, dass jedem Emittenten die Verantwortung für die Bewältigung eines Teils des globalen Problems zugeschrieben wird. Quantifizierbar wir das durch ein Budget. \n Einerseits möchten wir für die konkrete Bestimmung des Budgets berücksichtigen, dass der Zeitpunkt des Pariser Abkommens nahelegt, das globale Budget ab 2016 aufzuteilen. Andererseits streben wir danach, die aktuellsten und genauesten Berechnungen des tatsächlichen globalen Budgets einzubeziehen, um die Erfüllung der primären Temperaturziele wahrscheinlicher zu machen. Die derzeit aussagekräftigste Information über das globale Budget von 2016 ergibt sich aus der Summe des aktuellsten verfügbaren Budgets aus 1) und der seitdem emittierten Menge an CO2 aus 2).'
        ]
    )

    text_glob_2016 = html.P(
        [
            "Aus einem ",
            html.A(
                "Bericht des IPCCs von 2021",
                href="https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf",
            ),
            f" (S.29) geht hervor, welche Menenge CO₂ die gesamte Menschheit ab dem Jahr {co2d.budget_latest_start_date.year} noch emittieren darf um die entsprechenden Temperaturziele (+1.5°C, +1.7°C, +2.0°C) mit einer entsprechenden Wahrscheinlichkeit (17%-83%) zu erreichen.",
        ]
    )
    table_emissions_glob_2016_to_latest = nice_temp_precent_table(
        co2d.df_emissions_glob_between_2016_and_latest.astype(str) + " kt",
        "table_emissions_global_from_2016_to_latest",
    )

    # Most accurate estimation for the wworldwide Budget starting at the beginning of 2016, just after the End of the Paris Agreement
    # table_glob_2016 = nice_temp_precent_table

    # HD
    table_hd = nice_temp_precent_table(
        co2d.df_budget_hd_kt.round(2).astype(str) + " kt", "table_budgets_hd"
    )
    text_regional_budget = html.P(
        [
            "In einer ",
            html.A(
                "Stellungnahme",
                href="https://www.umweltrat.de/SharedDocs/Downloads/DE/04_Stellungnahmen/2020_2024/2022_06_fragen_und_antworten_zum_co2_budget.pdf?__blob=publicationFile&v=33",
            ),
            " (Kapitel 9) geht der Sachverständigenrat für Umweltfragen im Detail darauf ein, warum eine Aufteilung des globalen Budgets auf e.g. Nationalstaaten nach deren Bevölkerungsanteil 'ethisch gut begründet', 'praktikabel', und 'sachgerecht' ist. Im Vergleich zum globalen Budget, dass auf haten Wissenschaftlichen Analysen basiert ist ein Budget für e.g. Nationalstaaten immer ein menschen gemachtes Konstrukt. Hier ist nicht mehr die Frage nach korrekt oder falsch relevant. Vielmehr ist hier die Frage nach der Nützlichkeit die prägende. In der oben schon genannten ",
            html.A(
                "Stellungnahme",
                href="https://www.umweltrat.de/SharedDocs/Downloads/DE/04_Stellungnahmen/2020_2024/2022_06_fragen_und_antworten_zum_co2_budget.pdf?__blob=publicationFile&v=33",
            ),
            " (Kapitel 19) ghet der Sachverständigenrat für Umweltfragen auf die Bedenken ein, die mit einer Bevölkerungsanteiligen Aufteilung des Budgets auf e.g. Bundesländer oder Kommunen enhergehen. Er kommt aber letztlich auch zu dem Schluss dass durch die Einführung des Budget Ansatzes auch unterhalb der Ebene der Nationalstaaten: '...überall dort, wo klimarelevante Entscheidungen getroffen werden, ein Maßstab für einen ausreichenden, angemessenen und gerechten Beitrag geschaffen werden.'",
            html.P(),
            "Zur konkreten Berechnung können wir e.g. von ",
            html.A(
                "Statista",
                href="https://de.statista.com/statistik/daten/studie/1694/umfrage/entwicklung-der-weltbevoelkerungszahl/",
            ),
            " die Bevölkerungszahl der gesamten Erde heranziehen (Im Jahr 2020: 7,84 Milliarden). Ebenfalls von ",
            html.A(
                "Statista",
                href="https://de.statista.com/statistik/daten/studie/375849/umfrage/entwicklung-der-gesamtbevoelkerung-in-heidelberg/",
            ),
            " bekommen wir die Zahl der Heidelberger Bürger*innen (Im Jahr 2020: 158741). Daraus ergibt sich dass Heidelberg einen Anteil von c.a. 0,002% der Weltbevölkerung stellt. Das oben gezeigte Budget ist entsprechend anteilig vom globalen Budget aus 3) gerechnet.",
        ]
    )

    # HD Bisko
    table_hd_bisko = nice_temp_precent_table(
        co2d.df_budget_hd_bisko_kt.round(2).astype(str) + " kt",
        "table_budgets_hd_bisko",
    )
    text_hd_bisko = html.P(
        [
            "Das in 2) beschriebene Heidelberger Budget umfasst alle von Heidelberger Bürgern verursachten Emissionen. Die Stadt Heidelberg misst, wie viele andere Staedte auch, ihre Emissionen nach der ",
            html.A(
                "BISKO Systematik",
                href="https://www.kea-bw.de/fileadmin/user_upload/Energiemanagement/Angebote/Beschreibung_der_BISKO-Methodik.pdf",
            ),
            ". Der ",
            html.A(
                "C02 Bilanzierung bis 2018 für die Stadt Heidelberg",
                "https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents_E2103137505/heidelberg/Objektdatenbank/31/PDF/01_Ifeu_Studie_CO2_Bilanzierung_bis_2018_fuer_die_Stadt_Heidelberg.pdf",
            ),
            " ist zu entnehmen, dass die 'BISKO-Emissionen' rund 64% der von den Heidelbergern insgesammt verursachten Emissionen entsprechen. Um dem Rechnung zu tragen müssen wir auch das Heidelberger CO₂ Budget differenziert betrachten. Ein Teil des Budgets, nämlich genau die 64% kann für BISKO-Emissionen aufgewendet werden. Der Rest ist den Nicht-BISKO Emissionen vorbehalten. Entsprechend dieser Überlegung sind in der Tabelle oben die Heidelberger BISKO-Budgets aufgelistet.",
        ]
    )

    # HD Remaining
    table_hd_remaining_tonns = nice_temp_precent_table(
        (
            (co2d.df_budget_hd_bisko_kt - cumulated_emissions_this_second_plan(co2d))
            * 1000
        )
        .round(0)
        .astype(str)
        + " kt",
        "table_budgets_hd_bisko_remaining",
    )
    text_hd_remaining = html.P("Blubb BLubb HD Bisko Remaining")

    # HD Deplation Date
    df_date = co2d.df_budget_hd_bisko_kt.map(
        lambda x: when_budget_is_spend_plan_nicestr(co2d, x)
    )
    table_hd_deplation_date = nice_temp_precent_table(
        df_date.astype(str), "table_budgets_hd_bisko_deplation_date"
    )
    text_hd_depletion_date = html.P(
        [
            "Hier wird für jede Kombination aus gewünschter Temperaturerhöhung und der entsprechenden Wahrscheinlichkeit, diese auch tatsächlich zu erreichen, ein konkretes Datum genannt, an dem das entsprechende (BISKO-)Budget für Heidelberg voraussichtlich aufgebraucht sein wird. Dieses Datum ergibt sich aus den in 3) berechneten BISKO-Budgets sowie den im ",
            html.A(
                "Heidelberger Klimaschutzplan",
                href="https://app.climateview.global/v3/public/board/2ae7af89-40d4-4ff0-892c-febbfb36886f",
            ),
            " bisher gemessenen und zukünftig geplanten Emissionen. Nur die Kombinationen aus Temperatur und Wahrscheinlichkeit, die als 'nicht aufgebraucht' markiert sind, sind nach den aktuellen Klimaschutzplänen erreichbar.",
        ]
    )

    t = html.Div(
        [
            dcc.Tabs(
                id="tabs-123",
                value="tab-6",
                children=[
                    dcc.Tab(
                        label=f"1) Globales Budget ab {co2d.budget_latest_start_date.year}",
                        value="tab-1",
                    ),
                    dcc.Tab(
                        label=f"2) Globale Emissionen 2016 - {co2d.budget_latest_start_date.year - 1}",
                        value="tab-2",
                    ),
                    dcc.Tab(label="3) Globales Budget ab 2016", value="tab-3"),
                    dcc.Tab(label="4) Gesammt Budget HD ab 2016", value="tab-4"),
                    dcc.Tab(label="5) Bisko Budget HD ab 2016", value="tab-5"),
                    dcc.Tab(label="6) Budget Ende", value="tab-6"),
                    # dcc.Tab(label="Remaining Budget", value="tab-6"),
                ],
            ),
            html.Div(id="tabs-content"),
        ]
    )

    # TODO: Somehow it does not work with both inputs. only tabs is working
    @app.callback(
        Output("tabs-content", "children"),
        [Input("interval-component", "n_intervals"), Input("tabs-123", "value")],
    )
    def render_content(n_intervals, tab):
        if tab == "tab-1":
            return html.Div([html.P(), table_glob_latest, html.P(), text_glob_latest])
        elif tab == "tab-2":
            return html.Div(
                [
                    html.P(),
                    table_emissions_glob_2016_to_latest,
                    html.P(),
                    text_emissions_global_from2016,
                ]
            )
        elif tab == "tab-3":
            return html.Div(
                [html.P(), table_global_budget_2016, html.P(), text_global_budget_2016]
            )
        elif tab == "tab-4":
            return html.Div([html.P(), table_hd, html.P(), text_regional_budget])
        elif tab == "tab-5":
            return html.Div([html.P(), table_hd_bisko, html.P(), text_hd_bisko])
        elif tab == "tab-6":
            return html.Div(
                [html.P(), table_hd_deplation_date, html.P(), text_hd_depletion_date]
            )
        # elif tab == "tab-6":
        #     return html.Div([table_hd_remaining_tonns, html.P(), text_hd_remaining])

    card_table = dbc.Card(
        dbc.CardBody(
            [
                html.P(),
                html.H5("CO₂ Budgets"),
                html.P(
                    'Die interessanten Informationen sind im hier im Tab "6) Budget Ende" dargestellt. Zur Gewährleistung der Transparenz werden die Berechnungslogik sowie sämtliche Quellen und Zwischenergebnisse optional in den Tabs 1) bis 5) dargestellt.'
                ),
                t,
            ]
        )
    )

    return app, card_table
