from dataclasses import dataclass
import pandas as pd
from data.read_data import read_emissions
from data.target import add_targets
from data.trend import add_trend
from scenarios import (
    add_scenarios,
    when_scenario_0,
    cumulated_emissions,
    cumulated_emissions_this_second,
    when_budget_is_spend,
)


@dataclass
class data:
    df_balance: pd.DataFrame
    # df_budget_global_kt: pd.DataFrame
    # df_budget_hd_kt: pd.DataFrame
    # df_budget_hd_bisko_kt: pd.DataFrame
    # df_budget_hd_bisko_depleted_date: pd.DataFrame


# data
df_emissions = read_emissions()
df_emissions = df_emissions
df_emissions["co2_kt_total"] = df_emissions.sum(axis=1)

df_emissions = add_trend(df_emissions)
df_emissions = add_targets(df_emissions)

df_emissions = add_scenarios(df_emissions)


d = data(df_balance=df_emissions)
