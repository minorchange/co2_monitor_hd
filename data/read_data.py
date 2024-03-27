import pandas as pd
import json
from datetime import datetime
import os


def read_emissions_hd():
    print(os.getcwd())
    print(os.listdir(os.getcwd()))
    df_allbuttraffic = pd.read_csv("data/raw/co2_emissions_hd.csv", index_col=0).fillna(
        0
    )
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

    df_traffic = pd.read_csv("data/raw/co2_emissions_hd_traffic.csv", index_col=0)
    df_all = df_allbuttraffic.join(df_traffic, how="outer").interpolate(
        limit_direction="both"
    )
    return df_all


def read_emissions_global_t():
    emissions_global = pd.read_csv(
        "data/raw/co2_emissions_world_byyear_ourworldindata.csv", index_col=0
    )
    return emissions_global


def emissions_global_between_20016_and_latest_kt():
    df_emissions_glob = read_emissions_global_t()
    _, start_date = read_global_budget_latest_kt_df()
    sum_kt = (
        df_emissions_glob.loc[2016 : start_date.year - 1, "emissions_t"].sum() / 1000
    )
    return sum_kt


def emissions_global_between_20016_and_latest_table_kt():
    df_glob, start_date = read_global_budget_latest_kt_df()

    sum = emissions_global_between_20016_and_latest_kt()
    df_sum = df_glob.replace(to_replace=df_glob.values, value=sum)
    return df_sum


def read_plan_from_csv():
    df_plan = pd.read_csv("data/raw/hd_emissions_plan_bisko.csv", index_col=0)
    return df_plan


def read_global_budget_latest_kt_df():
    with open(
        "data/raw/co2_budget_ipcc_2021_physical_science_basis_summary_for_policymakers.json",
        "r",
    ) as json_file:
        data_json = json.load(json_file)

    Gt2kt = 1000000
    df_read = pd.DataFrame(data_json["dataframe"]) * Gt2kt
    df_read.set_index(pd.Index(data_json["index"]), inplace=True)
    # first_year_the_budget_is_spend = data_json["first_year_the_budget_is_spend"]
    start_date = datetime.strptime(data_json["start_date"], data_json["date_format"])
    return df_read, start_date


def global_budget_2016_kt_df():
    df_latest, _ = read_global_budget_latest_kt_df()
    df_emissions = emissions_global_between_20016_and_latest_table_kt()
    df_budget_2016 = df_latest + df_emissions
    return df_budget_2016


def bisko_underestimate_factor():
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

    return buf


def total_budget_to_bisko_budget(b):
    buf = bisko_underestimate_factor()
    bisko_budget = b * buf
    return bisko_budget


def read_budget():
    df_budget = pd.read_csv("data/raw/co2_budget_hd_newclimate.csv", index_col=False)
    budget_start_year = df_budget.first_year_the_budget_is_spend.values[0]
    budget_start_value_kt = df_budget.co2_budget_kt.values[0]
    return budget_start_year, budget_start_value_kt


def portion_of_population_hd_2020():
    global_population = 7840000000  # https://de.statista.com/statistik/daten/studie/1694/umfrage/entwicklung-der-weltbevoelkerungszahl/
    hd_population = 158741  # https://de.statista.com/statistik/daten/studie/375849/umfrage/entwicklung-der-gesamtbevoelkerung-in-heidelberg/
    ratio = float(hd_population) / float(global_population)
    return ratio


def read_budget_2016_hd_kt_df():
    start_date = 2016
    df_glob = global_budget_2016_kt_df()
    df_hd_kt = df_glob * portion_of_population_hd_2020()
    return df_hd_kt, start_date


def read_bisko_budget_2016_hd_kt_df():
    df_hd, start_date = read_budget_2016_hd_kt_df()
    df_hd_bisko_kt = df_hd * bisko_underestimate_factor()
    return df_hd_bisko_kt, start_date


def read_bisko_budget():
    budget_start_year, budget_start_value_kt = read_budget()
    bisko_budget_start_value_kt = total_budget_to_bisko_budget(budget_start_value_kt)
    return budget_start_year, bisko_budget_start_value_kt


if __name__ == "__main__":
    budget_start_year, budget_start_value_kt = read_bisko_budget()
    print(budget_start_year, budget_start_value_kt)
    df_hd_bisko_kt, start_date = read_bisko_budget_2016_hd_kt_df()
    print(df_hd_bisko_kt, start_date)
    read_plan_from_csv()
