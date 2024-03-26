import os, sys
import datetime
from dateutil.relativedelta import relativedelta
from data.read_data import read_bisko_budget
from components.scenarios import (
    emissions_measured_or_planned,
    when_budget_is_spend_plan,
)
import numpy as np


def get_remaining_paris_budget_next_deadline(co2d):

    now = datetime.datetime.now()

    # df_date = co2d.df_budget_hd_bisko_kt.map(
    #     lambda x: when_budget_is_spend_plan(co2d, x)
    # )
    # next_deadline = df_date[df_date > now].min().min()

    # row_index = df_date.index[df_date.isin([next_deadline]).any(axis=1)][0]
    # col_index = df_date.columns[df_date.isin([next_deadline]).any()][0]

    # return (
    #     remaining_budget_kt,
    #     when_budget_is_depleted,
    #     row_index,
    #     col_index,
    # )

    df_emissions = emissions_measured_or_planned(co2d)

    def _contribution_of_all_completed_years(df_emissions):

        last_year = now.year - 1

        df_fully = df_emissions[
            (df_emissions.index <= last_year) & (df_emissions.index >= 2016)
        ]

        total_emissions_full_years_kt = df_fully.sum()
        return total_emissions_full_years_kt

    def _contribution_of_current_year(df_emissions):
        this_year_completion_factor = (
            now - datetime.datetime(now.year, 1, 1)
        ).total_seconds() / (60 * 60 * 24 * 365.25)
        emissions_this_year_so_far_kt = (
            df_emissions.loc[now.year] * this_year_completion_factor
        )
        return emissions_this_year_so_far_kt

    all_emissions_up_to_now_kt = _contribution_of_all_completed_years(
        df_emissions
    ) + _contribution_of_current_year(df_emissions)

    def find_smallest_non_zero_values(df):
        min_value = df[df >= 0].min().min()
        min_index = np.where(df == min_value)

        row_index = min_index[0][0]
        col_index = min_index[1][0]

        return min_value, df.index[row_index], df.columns[col_index]

    remaining_budget_kt, row_index, col_index = find_smallest_non_zero_values(
        co2d.df_budget_hd_bisko_kt - all_emissions_up_to_now_kt
    )

    original_budget_that_is_now_closest_to_beeing_depleted = (
        co2d.df_budget_hd_bisko_kt.loc[row_index, col_index]
    )
    when_budget_is_depleted = when_budget_is_spend_plan(
        co2d, original_budget_that_is_now_closest_to_beeing_depleted
    )

    return (
        remaining_budget_kt,
        when_budget_is_depleted,
        row_index,
        col_index,
    )


def get_remaining_paris_budget(df):
    assert "co2_kt_total" in df.columns

    budget_start_year, bisko_budget_start_value_kt = read_bisko_budget()

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

    remaining_budget_kt = bisko_budget_start_value_kt - total_emissions_kt
    remaining_seconds = remaining_budget_kt / latest_emissions_ktpersecond

    when_budget_is_depleted = now + relativedelta(seconds=+remaining_seconds)
    return remaining_budget_kt, when_budget_is_depleted


if __name__ == "__main__":
    from read_data import read_emissions_hd

    df_emissions = read_emissions_hd()
    remaining_budget_kt, when_budget_is_depleted = get_remaining_paris_budget(
        df_emissions, trend
    )

    print(total_emissions_kt)
    print(remaining_budget_kt)
    print(remaining_budget_kt.year)
