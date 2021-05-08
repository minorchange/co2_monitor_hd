import numpy as np
import datetime
from dateutil.relativedelta import relativedelta


def add_scenarios(df):

    assert "co2_kt_total" in df.columns
    assert "trend_const_kt" in df.columns
    assert "trend_lin_kt" in df.columns

    df["scenario_trendlin_kt"] = df["co2_kt_total"].fillna(df["trend_lin_kt"])
    df["scenario_trendconst_kt"] = df["co2_kt_total"].fillna(df["trend_const_kt"])

    df["scenario_target30_kt"] = df["co2_kt_total"].fillna(df["target30_kt"]).fillna(0)
    df["scenario_target50_kt"] = df["co2_kt_total"].fillna(df["target50_kt"]).fillna(0)
    df["scenario_target30_new_kt"] = (
        df["co2_kt_total"].fillna(df["target30_new_kt"]).fillna(0)
    )
    df["scenario_target50_new_kt"] = (
        df["co2_kt_total"].fillna(df["target50_new_kt"]).fillna(0)
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
