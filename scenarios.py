import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import math


def add_scenarios(df):
    assert "co2_kt_total" in df.columns
    assert "trend_const_kt" in df.columns
    assert "trend_lin_kt" in df.columns

    df["scenario_trendlin_kt"] = df["co2_kt_total"].fillna(df["trend_lin_kt"])
    df["scenario_trendconst_kt"] = df["co2_kt_total"].fillna(df["trend_const_kt"])

    df["scenario_target30_kt"] = df["co2_kt_total"].fillna(df["target30_kt"]).fillna(0)
    df["scenario_target40_kt"] = df["co2_kt_total"].fillna(df["target40_kt"]).fillna(0)
    df["scenario_target30_new_kt"] = (
        df["co2_kt_total"].fillna(df["target30_new_kt"]).fillna(0)
    )
    df["scenario_target40_new_kt"] = (
        df["co2_kt_total"].fillna(df["target40_new_kt"]).fillna(0)
    )

    return df


def when_scenario_0(df, scenario_name):
    s = df[scenario_name]
    assert not s.isnull().any()

    first_y_when_data_is_0 = s.index[s == 0].min()
    if np.isnan(first_y_when_data_is_0):
        first_y_when_data_is_0 = np.inf
    return first_y_when_data_is_0


def cumulated_emissions(df, scenario_name, from_y=None, to_y=None):
    s = df[scenario_name]
    assert not s.isnull().any()

    if from_y is not None:
        s = s[s.index >= from_y]
    if to_y is not None:
        s = s[s.index <= to_y]

    sum = s.sum()

    if when_scenario_0(df, scenario_name) == np.inf:
        sum = np.inf

    return sum


def all_relevant_measured_emissions(co2d):
    last_year_with_measured_data = (
        co2d.df_emissions_hd.co2_kt_total.dropna().index.max()
    )

    where_balance_after_budget_start = (
        co2d.df_emissions_hd.co2_kt_total.index >= co2d.budget_latest_start_date.year
    )
    where_balance_measured_data_available = (
        co2d.df_emissions_hd.co2_kt_total.index <= last_year_with_measured_data
    )

    all_relevant_years_with_measured_data = co2d.df_emissions_hd.loc[
        where_balance_after_budget_start & where_balance_measured_data_available,
        "co2_kt_total",
    ]

    measured_sum = all_relevant_years_with_measured_data.sum()
    return measured_sum


def all_relevant_concluded_planned_years(co2d):
    last_year_with_measured_data = (
        co2d.df_emissions_hd.co2_kt_total.dropna().index.max()
    )

    df_plan = co2d.df_plan

    now = datetime.datetime.now()
    assert co2d.budget_latest_start_date < now
    current_year = now.year

    where_no_measured_data_exists = df_plan.index > last_year_with_measured_data
    where_planned_years_are_concluded = df_plan.index < current_year

    all_relevant_planned_concluded_years = df_plan.loc[
        where_no_measured_data_exists & where_planned_years_are_concluded,
        "planned emissions",
    ]
    relevant_planned_concluded_sum = all_relevant_planned_concluded_years.sum()
    return relevant_planned_concluded_sum


def fraction_current_year_plan(co2d):
    now = datetime.datetime.now()
    current_year = now.year
    first_sec_of_current_year_str = f"{current_year}-01-01 00:00:00"
    first_sec_of_current_year = datetime.datetime.strptime(
        first_sec_of_current_year_str, "%Y-%m-%d %H:%M:%S"
    )
    seconds_this_year_so_far = (now - first_sec_of_current_year).total_seconds()
    this_year_complete_fraction = seconds_this_year_so_far / (60 * 60 * 24 * 365.2)

    emissions_this_year = float(co2d.df_plan.loc[current_year].values)
    emissions_this_year_so_far = emissions_this_year * this_year_complete_fraction

    return emissions_this_year_so_far


def cumulated_emissions_this_second_plan(co2d):
    measured_emissions = all_relevant_measured_emissions(co2d)
    concluded_planned_years_emissions = all_relevant_concluded_planned_years(co2d)
    this_year_fraction_emissions = fraction_current_year_plan(co2d)
    cumulated_emissions_so_far = (
        measured_emissions
        + concluded_planned_years_emissions
        + this_year_fraction_emissions
    )
    return cumulated_emissions_so_far


def emissions_measured_or_planned(co2d):
    df_prio = co2d.df_emissions_hd.co2_kt_total.dropna()
    df_secondary = co2d.df_plan["planned emissions"]
    df = df_prio.combine_first(df_secondary)
    return df


def cumulated_emissions_this_second(df, scenario_name, from_y):
    s = df[scenario_name]
    assert not s.isnull().any()

    if from_y is not None:
        s = s[s.index >= from_y]

    now = datetime.datetime.now()
    current_year = now.year

    first_sec_of_current_year_str = f"{current_year}-01-01 00:00:00"
    first_sec_of_current_year = datetime.datetime.strptime(
        first_sec_of_current_year_str, "%Y-%m-%d %H:%M:%S"
    )
    seconds_this_year_so_far = (now - first_sec_of_current_year).total_seconds()
    this_year_complete_fraction = seconds_this_year_so_far / (60 * 60 * 24 * 365.2)

    cumulated_emissions_past_years = s[s.index < current_year].sum()
    emissions_this_year = s[current_year]
    emissions_this_year_so_far = emissions_this_year * this_year_complete_fraction

    cumulated_emissions_so_far = (
        cumulated_emissions_past_years + emissions_this_year_so_far
    )

    return cumulated_emissions_so_far


def when_budget_is_spend(df, scenario_name, budget_kt, from_y):
    s = df[scenario_name]
    assert not s.isnull().any()
    s = s[s.index >= from_y]

    first_year_the_budget_is_depleted = s.index[s.cumsum() > budget_kt].min()

    return first_year_the_budget_is_depleted


def when_budget_is_spend_plan(co2d, budget_kt):
    # df_plan = co2d.df_plan
    # df_plan = df_plan[df_plan.index >= 2016]
    df_measure_or_plan = emissions_measured_or_planned(co2d)
    df_measure_or_plan = df_measure_or_plan.loc[df_measure_or_plan.index >= 2016]

    def first_year_the_budget_is_depleted(budget_kt):
        first_year_the_budget_is_depleted = df_measure_or_plan.index[
            df_measure_or_plan.cumsum() > budget_kt
        ].min()
        return first_year_the_budget_is_depleted

    def year_before_budget_is_depleted(budget_kt):
        return first_year_the_budget_is_depleted(budget_kt) - 1

    if math.isnan(first_year_the_budget_is_depleted(budget_kt)):
        return None

    s = df_measure_or_plan
    assert not s.isnull().any()
    s = s[s.index >= 2016]
    s = s[s.index <= year_before_budget_is_depleted(budget_kt)]

    sum_whole_years = s.sum()
    assert sum_whole_years > 0
    # assert sum_whole_years < budget_kt

    emissions_in_depletion_year = emissions_measured_or_planned(co2d)[
        first_year_the_budget_is_depleted(budget_kt)
    ]

    # assert budget_kt - sum_whole_years >= 0
    assert budget_kt - sum_whole_years < emissions_in_depletion_year

    fraction_of_depletion_year = (
        budget_kt - sum_whole_years
    ) / emissions_in_depletion_year
    assert fraction_of_depletion_year >= 0
    assert fraction_of_depletion_year < 1

    def date_from_year_fraction(fraction, year):
        if not (0 <= fraction < 1):
            raise ValueError("Fraction should be between 0 and 1")

        now = datetime.datetime.now()
        year_start = datetime.datetime(year, 1, 1)

        days_passed = int((fraction) * 365)  # Assuming a non-leap year

        target_date = year_start + datetime.timedelta(days=days_passed)

        return target_date

    date_budget_is_depleted = date_from_year_fraction(
        fraction_of_depletion_year, first_year_the_budget_is_depleted(budget_kt)
    )

    return date_budget_is_depleted


def when_budget_is_spend_plan_nicestr(co2d, budget_kt):
    date_budget_is_depleted = when_budget_is_spend_plan(co2d, budget_kt)
    if date_budget_is_depleted is None:
        return "Nicht aufgebraucht"
    else:
        return date_budget_is_depleted.strftime("%d.%m.%Y")
