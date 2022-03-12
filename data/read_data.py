import pandas as pd


def read_emissions():

    df_allbuttraffic = pd.read_csv("data/raw/co2_hd.csv", index_col=0).fillna(0)
    df_allbuttraffic["co2_kt_gewerbe_u_oeffentlgeb"] = (
        df_allbuttraffic.co2_kt_gewerbe + df_allbuttraffic.co2_kt_oeffentlgeb
    )
    df_allbuttraffic = df_allbuttraffic[
        [
            "co2_kt_privatehh",
            "co2_kt_industrie",
            "co2_kt_staedtgeb",
            "co2_kt_gewerbe_u_oeffentlgeb",
            "co2_kt_sum",
        ]
    ]

    sum_sanity_check = df_allbuttraffic[
        [
            "co2_kt_privatehh",
            "co2_kt_industrie",
            "co2_kt_staedtgeb",
            "co2_kt_gewerbe_u_oeffentlgeb",
        ]
    ].sum(axis=1)
    assert (sum_sanity_check == df_allbuttraffic.co2_kt_sum).all()
    df_allbuttraffic = df_allbuttraffic[
        [
            "co2_kt_privatehh",
            "co2_kt_industrie",
            "co2_kt_staedtgeb",
            "co2_kt_gewerbe_u_oeffentlgeb",
        ]
    ]

    df_traffic = pd.read_csv("data/raw/co2_hd_traffic.csv", index_col=0)
    df_all = df_allbuttraffic.join(df_traffic, how="outer").interpolate(
        limit_direction="both"
    )
    return df_all


def total_budget_to_bisko_budget(b):
    # https://de.statista.com/statistik/daten/studie/375849/umfrage/entwicklung-der-gesamtbevoelkerung-in-heidelberg/
    persons_living_in_hd_2015 = 156267
    # https://www.heidelberg.de/site/Heidelberg_ROOT/get/documents_E2103137505/heidelberg/Objektdatenbank/31/PDF/01_Ifeu_Studie_CO2_Bilanzierung_bis_2018_fuer_die_Stadt_Heidelberg.pdf
    total_average_emissions_one_person_2015_tons = 11.2
    bisko_emissions_hd_2015_tons = 1117433

    bisko_average_emissions_one_person_2015_tons = float(
        bisko_emissions_hd_2015_tons
    ) / float(persons_living_in_hd_2015)
    biso_underestimate_factor = (
        bisko_average_emissions_one_person_2015_tons
        / total_average_emissions_one_person_2015_tons
    )
    buf = biso_underestimate_factor
    assert buf > 0
    assert buf < 1
    # in 2015 the emissions covered by the bisko standard were buf * total emissions
    # buf is around 0.64
    # Since no up to date values could be found we assume that the ratio between emissions
    # measured by bisko and total emissions are constant over time.
    # Therefore the total bugdet must be devided in a bisko budget and a non bisko budget.

    bisko_budget = b * buf
    return bisko_budget


def read_budget():
    df_budget = pd.read_csv("data/raw/co2_budget_hd.csv", index_col=False)
    budget_start_year = df_budget.first_year_the_budget_is_spend.values[0]
    budget_start_value_kt = df_budget.co2_budget_kt.values[0]
    return budget_start_year, budget_start_value_kt


def read_bisko_budget():
    budget_start_year, budget_start_value_kt = read_budget()
    bisko_budget_start_value_kt = total_budget_to_bisko_budget(budget_start_value_kt)
    return budget_start_year, bisko_budget_start_value_kt


if __name__ == "__main__":
    budget_start_year, budget_start_value_kt = read_bisko_budget()
    print(budget_start_year, budget_start_value_kt)
