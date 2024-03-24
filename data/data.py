from dataclasses import dataclass
import pandas as pd
from data.read_data import (
    read_emissions_hd,
    read_global_budget_latest_kt_df,
    global_budget_2016_kt_df,
    read_budget_2016_hd_kt_df,
    read_bisko_budget_2016_hd_kt_df,
    read_plan_from_csv,
    emissions_global_between_20016_and_latest_table_kt,
)
from data.target import add_targets
from data.trend import add_trend
from scenarios import (
    add_scenarios,
    when_scenario_0,
    cumulated_emissions,
    cumulated_emissions_this_second,
    when_budget_is_spend,
)
import datetime


@dataclass
class co2data:
    df_emissions_hd: pd.DataFrame
    df_plan: pd.DataFrame
    df_emissions_glob_between_2016_and_latest: pd.DataFrame
    df_budget_latest_global_kt: pd.DataFrame
    df_budget_2016_global_kt: pd.DataFrame
    df_budget_hd_kt: pd.DataFrame
    df_budget_hd_bisko_kt: pd.DataFrame
    budget_latest_start_date: datetime.datetime
    # df_budget_hd_bisko_depleted_date: pd.DataFrame


# data
df_emissions_hd = read_emissions_hd()
df_emissions_hd["co2_kt_total"] = df_emissions_hd.sum(axis=1)
df_emissions_hd = add_trend(df_emissions_hd)
df_emissions_hd = add_targets(df_emissions_hd)
df_emissions_hd = add_scenarios(df_emissions_hd)


df_budget_global_latest_kt, budget_global_latest_start_date = (
    read_global_budget_latest_kt_df()
)
df_budget_hd_2016_kt, budget_hd_start_date = read_budget_2016_hd_kt_df()
df_budget_hd_2016_bisko_kt, budget_hd_bisko_start_date = (
    read_bisko_budget_2016_hd_kt_df()
)

df_plan = read_plan_from_csv()

co2d = co2data(
    df_emissions_hd=df_emissions_hd,
    df_plan=df_plan,
    df_emissions_glob_between_2016_and_latest=emissions_global_between_20016_and_latest_table_kt(),
    df_budget_latest_global_kt=df_budget_global_latest_kt,
    df_budget_2016_global_kt=global_budget_2016_kt_df(),
    df_budget_hd_kt=df_budget_hd_2016_kt,
    df_budget_hd_bisko_kt=df_budget_hd_2016_bisko_kt,
    budget_latest_start_date=budget_global_latest_start_date,
)
