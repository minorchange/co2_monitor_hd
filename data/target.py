import pandas as pd
import numpy as np


def create_target_line(start_year, target_year, df_emissions):
    assert target_year > start_year
    assert target_year < 3000
    assert start_year in df_emissions.index

    df = pd.DataFrame({"year": range(start_year, target_year + 1)})
    df["target"] = np.nan
    df = df.set_index("year")
    val_at_startdate = df_emissions.sum(axis=1)[start_year]
    df.loc[start_year, "target"] = val_at_startdate
    df.loc[target_year, "target"] = 0
    df = df.interpolate()
    df_res = df[df.index >= df_emissions.index.min()]

    return df_res


def compare_emissions_with_target(df_emissions, df_t30, df_t50):

    df_compare_with_target = pd.DataFrame(df_emissions.sum(axis=1))

    df_compare_with_target = pd.DataFrame(df_emissions.sum(axis=1))
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


def compute_new_line_targets(df_emissions):

    df_t30 = create_target_line(2014, 2030, df_emissions)
    df_t50 = create_target_line(2014, 2050, df_emissions)

    df_compare_with_target = compare_emissions_with_target(df_emissions, df_t30, df_t50)

    last_year_with_data = df_compare_with_target.index.max()
    last_emissions = df_compare_with_target.actual_emissions[last_year_with_data]

    emissions_so_far = df_compare_with_target["actual_emissions"].sum()
    # overshoot_emissions30 = df_compare_with_target["diff30"].sum()
    # overshoot_emissions50 = df_compare_with_target["diff50"].sum()
    planned_lin30_emissions = df_t30["target"].sum()
    planned_lin50_emissions = df_t50["target"].sum()
    remaining_emissions30 = planned_lin30_emissions - emissions_so_far
    remaining_emissions50 = planned_lin50_emissions - emissions_so_far

    new_lin_target_30_years = remaining_emissions30 / (last_emissions / 2)
    new_lin_target_50_years = remaining_emissions50 / (last_emissions / 2)
    new_lin_target_30 = int(last_year_with_data + new_lin_target_30_years)
    new_lin_target_50 = int(last_year_with_data + new_lin_target_50_years)

    df_t30_new = create_target_line(
        last_year_with_data, new_lin_target_30, df_emissions
    )
    df_t50_new = create_target_line(
        last_year_with_data, new_lin_target_50, df_emissions
    )
    return (
        df_compare_with_target,
        df_t30,
        df_t50,
        new_lin_target_30,
        new_lin_target_50,
        df_t30_new,
        df_t50_new,
    )


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
