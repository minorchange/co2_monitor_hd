import os, sys
import datetime
from dateutil.relativedelta import relativedelta
from data.read_data import read_budget


def get_remaining_paris_budget(df):

    assert "co2_kt_total" in df.columns

    budget_start_year, budget_start_value_kt = read_budget()

    s_total = df["co2_kt_total"].dropna()

    s_measured_since_budgetstart = s_total[s_total.index >= budget_start_year]
    measured_co2kt_since_budgetstart = s_measured_since_budgetstart.sum()

    last_measured_year = s_total.index.max()
    latest_emissions_ktperyear = s_total[last_measured_year]
    assert latest_emissions_ktperyear > -1
    assert latest_emissions_ktperyear < 3000

    seconds_per_year = 60 * 60 * 24 * 365.25
    latest_emissions_ktpersecond = latest_emissions_ktperyear / seconds_per_year

    last_measured_year_since_before_budgetstart = max(
        last_measured_year, budget_start_year - 1
    )
    last_measured_second = datetime.datetime.strptime(
        f"{last_measured_year_since_before_budgetstart}-12-31 23:59:59",
        "%Y-%m-%d %H:%M:%S",
    )

    now = datetime.datetime.now()
    seconds_since_last_measured_second = (now - last_measured_second).total_seconds()

    estimated_emissions_kt = (
        latest_emissions_ktpersecond * seconds_since_last_measured_second
    )
    total_emissions_kt = measured_co2kt_since_budgetstart + estimated_emissions_kt

    remaining_budget_kt = budget_start_value_kt - total_emissions_kt
    remaining_seconds = remaining_budget_kt / latest_emissions_ktpersecond

    when_budget_is_depleted = now + relativedelta(seconds=+remaining_seconds)
    return remaining_budget_kt, when_budget_is_depleted


# def get_remaining_paris_budget(df_emissions, df_trend):

#     budget_start_year, budget_start_value_kt = read_budget()

#     df_measured_since_budgetstart = df_emissions[
#         df_emissions.index >= budget_start_year
#     ]
#     measured_co2kt_since_budgetstart = df_measured_since_budgetstart.sum().sum()

#     last_measured_year = df_emissions.index.max()
#     latest_emissions_ktperyear = df_emissions.loc[df_emissions.index.max()].sum()
#     assert latest_emissions_ktperyear > -1
#     assert latest_emissions_ktperyear < 3000

#     seconds_per_year = 60 * 60 * 24 * 365.25
#     latest_emissions_ktpersecond = latest_emissions_ktperyear / seconds_per_year

#     last_measured_year_since_before_budgetstart = max(
#         last_measured_year, budget_start_year - 1
#     )
#     last_measured_second = datetime.datetime.strptime(
#         f"{last_measured_year_since_before_budgetstart}-12-31 23:59:59",
#         "%Y-%m-%d %H:%M:%S",
#     )

#     now = datetime.datetime.now()
#     seconds_since_last_measured_second = (now - last_measured_second).total_seconds()

#     estimated_emissions_kt = (
#         latest_emissions_ktpersecond * seconds_since_last_measured_second
#     )
#     total_emissions_kt = measured_co2kt_since_budgetstart + estimated_emissions_kt

#     remaining_budget_kt = budget_start_value_kt - total_emissions_kt
#     remaining_seconds = remaining_budget_kt / latest_emissions_ktpersecond

#     when_budget_is_depleted = now + relativedelta(seconds=+remaining_seconds)
#     return remaining_budget_kt, when_budget_is_depleted

if __name__ == "__main__":

    from read_data import read_emissions

    df_emissions = read_emissions()
    remaining_budget_kt, when_budget_is_depleted = get_remaining_paris_budget(
        df_emissions, trend
    )

    print(total_emissions_kt)
    print(remaining_budget_kt)
    print(remaining_budget_kt.year)
