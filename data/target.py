import pandas as pd
import numpy as np


def create_target_line(start_year, target_year, s_t):
    assert target_year > start_year
    assert target_year < 3000
    assert start_year in s_t.index

    df = pd.DataFrame({"year": range(start_year, target_year + 1)})
    df["target"] = np.nan
    df = df.set_index("year")
    val_at_startdate = s_t[start_year]
    df.loc[start_year, "target"] = val_at_startdate
    df.loc[target_year, "target"] = 0
    df = df.interpolate()
    df_res = df[df.index >= s_t.index.min()]

    s_res = df_res["target"]
    return s_res


def compare_emissions_with_target(df_emissions, df_t30, df_t50):

    df_compare_with_target = pd.DataFrame(df_emissions.sum(axis=1))

    df_compare_with_target = pd.Datstart_yearaFrame(df_emissions.sum(axis=1))
    df_compare_with_target = df_compare_with_target.join(df_t30, how="inner").join(
        df_t50, how="inner", rsuffix="_"
    )
    df_compare_with_target.columns = ["actual_emissions", "target_2030", "target_2050"]

    df_compare_with_target["diff30"] = (
        df_compare_with_target["actual_emissions"]
        - df_compare_with_target["target_2030"]
    )
    df_compare_with_target["diff50"] = (
        df_compare_with_target["actual_emissions"]
        - df_compare_with_target["target_2050"]
    )

    df_compare_with_target["diff30cumsum"] = df_compare_with_target.diff30.cumsum()
    df_compare_with_target["diff50cumsum"] = df_compare_with_target.diff50.cumsum()

    return df_compare_with_target


def add_targets(df):

    assert "co2_kt_total" in df.columns
    target_start_year = 2014
    s_t = df["co2_kt_total"].dropna()
    s_t = s_t[s_t.index >= target_start_year]

    s_t30 = create_target_line(target_start_year, 2030, s_t)
    s_t50 = create_target_line(target_start_year, 2050, s_t)

    df["target30_kt"] = s_t30
    df["target50_kt"] = s_t50

    df["diff_target30_kt"] = df["co2_kt_total"] - df["target30_kt"]
    df["diff_target50_kt"] = df["co2_kt_total"] - df["target50_kt"]

    last_year_with_data = s_t.index.max()
    last_emissions = s_t[last_year_with_data]

    emissions_so_far = s_t.sum()
    # overshoot_emissions30 = df_compare_with_target["diff30"].sum()
    # overshoot_emissions50 = df_compare_with_target["diff50"].sum()
    planned_lin30_emissions = s_t30.sum()
    planned_lin50_emissions = s_t50.sum()
    remaining_emissions30 = planned_lin30_emissions - emissions_so_far
    remaining_emissions50 = planned_lin50_emissions - emissions_so_far

    new_equiemission_lin_target_30_years = remaining_emissions30 / (last_emissions / 2)
    new_equiemission_lin_target_50_years = remaining_emissions50 / (last_emissions / 2)
    new_equiemission_lin_target_30 = int(
        last_year_with_data + new_equiemission_lin_target_30_years
    )
    new_equiemission_lin_target_50 = int(
        last_year_with_data + new_equiemission_lin_target_50_years
    )
    s_t30_new_equiemission = create_target_line(
        last_year_with_data, new_equiemission_lin_target_30, s_t
    )
    s_t50_new_equiemission = create_target_line(
        last_year_with_data, new_equiemission_lin_target_50, s_t
    )

    s_t30_new = create_target_line(last_year_with_data, 2030, s_t)
    s_t50_new = create_target_line(last_year_with_data, 2050, s_t)

    df["target30_new_kt"] = s_t30_new
    df["target50_new_kt"] = s_t50_new

    return df


# def create_target_dfs(start_year, target_year_list, df_emissions):

#     target_fig_list = []
#     for ty in target_year_list:
#         df_t = create_target_line(start_year, ty, df_emissions)
#         fig_t = px.line(df_t, x=df_t.index, y=df_t.columns)
#         target_fig_list += fig_t

#         # df_t30 = create_target_line(2014, 2030, df_emissions)
#         # df_t50 = create_target_line(2014, 2050, df_emissions)

#         # fig_t30 = px.line(df_t30, x=df_t30.index, y=df_t30.columns)
#         # fig_t50 = px.line(df_t50, x=df_t50.index, y=df_t50.columns)

#         return target_fig_list
