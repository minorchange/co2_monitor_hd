from dataclasses import dataclass
import pandas as pd
from data.read_data import (
    read_emissions,
    read_global_budget_Gt_df,
    read_budget_hd_kt_df,
    read_bisko_budget_hd_kt_df,
    read_plan_from_csv,
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
    df_balance: pd.DataFrame
    df_plan: pd.DataFrame
    df_budget_global_kt: pd.DataFrame
    df_budget_hd_kt: pd.DataFrame
    df_budget_hd_bisko_kt: pd.DataFrame
    budget_start_date: datetime.datetime
    # df_budget_hd_bisko_depleted_date: pd.DataFrame


# data
df_emissions = read_emissions()
df_emissions["co2_kt_total"] = df_emissions.sum(axis=1)
df_emissions = add_trend(df_emissions)
df_emissions = add_targets(df_emissions)
df_emissions = add_scenarios(df_emissions)

df_budget_global_Gt, budget_global_start_date = read_global_budget_Gt_df()
df_budget_hd_kt, budget_hd_start_date = read_budget_hd_kt_df()
df_budget_hd_bisko_kt, budget_hd_bisko_start_date = read_bisko_budget_hd_kt_df()
assert budget_global_start_date == budget_hd_start_date == budget_hd_bisko_start_date
df_plan = read_plan_from_csv()
co2d = co2data(
    df_balance=df_emissions,
    df_plan=df_plan,
    df_budget_global_kt=df_budget_global_Gt * 1000000,
    df_budget_hd_kt=df_budget_hd_kt,
    df_budget_hd_bisko_kt=df_budget_hd_bisko_kt,
    budget_start_date=budget_global_start_date,
)
