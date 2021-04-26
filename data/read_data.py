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


def read_budget():
    df_budget = pd.read_csv("data/raw/co2_budget_hd.csv", index_col=False)
    budget_start_year = df_budget.first_year_the_budget_is_spend.values[0]
    budget_start_value_kt = df_budget.co2_budget_kt.values[0]
    return budget_start_year, budget_start_value_kt


if __name__ == "__main__":
    budget_start_year, budget_start_value_kt = read_budget()
    print(budget_start_year, budget_start_value_kt)