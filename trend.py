import pandas as pd
import numpy as np


def line(x1, y1, x2, y2, xrange_start, xrange_end, xindexname):

    assert x1 < x2
    assert xrange_start <= x1
    assert xrange_start < x2
    assert xrange_start < xrange_end
    assert x2 <= xrange_end

    ycolumnname = "y"
    df = pd.DataFrame({xindexname: range(xrange_start, xrange_end + 1)})
    df[ycolumnname] = np.nan
    df = df.set_index(xindexname)
    dx = x2 - x1
    dy = y2 - y1
    m = float(dy) / dx
    y_end = y2 + m * (xrange_end - x2)
    y_start = y2 - m * (x2 - xrange_start)
    df.loc[xrange_start, ycolumnname] = y_start
    df.loc[xrange_end, ycolumnname] = y_end

    df = df.interpolate(limit_direction="both")

    s = df[ycolumnname]
    return s


# def line(x1, y1, x2, y2, xrange_start, xrange_end, xindexname, ycolumnname):

#     assert x1 < x2
#     assert xrange_start <= x1
#     assert xrange_start < x2
#     assert xrange_start < xrange_end
#     assert x2 <= xrange_end

#     df = pd.DataFrame({xindexname: range(xrange_start, xrange_end + 1)})
#     df[ycolumnname] = np.nan
#     df = df.set_index(xindexname)
#     dx = x2 - x1
#     dy = y2 - y1
#     m = float(dy) / dx
#     y_end = y2 + m * (xrange_end - x2)
#     y_start = y2 - m * (x2 - xrange_start)
#     df.loc[xrange_start, ycolumnname] = y_start
#     df.loc[xrange_end, ycolumnname] = y_end

#     df = df.interpolate(limit_direction="both")

#     return df

# class LinTrend:
#     def __init__(self, x1, y1, x2, y2):

#         df_xrange_start = 2014
#         df_xrange_end = 2050

#         assert x1 < x2
#         assert df_xrange_start <= x1
#         assert df_xrange_start < x2
#         assert df_xrange_start < df_xrange_end
#         assert x2 <= df_xrange_end

#         # self.y_intercept = None
#         self.slope_y = float(y2 - y1) / float(x2 - x1)
#         self.slope_s = self.slope_y / (365.25 * 24 * 60 * 60)
#         self.df = line(x1, y1, x2, y2, df_xrange_start, df_xrange_end, "year", "trend")


def add_trend(df):

    assert "co2_kt_total" in df.columns

    s_t = df["co2_kt_total"].dropna()

    year_start = 2014
    assert 2014 in s_t.index
    year_end = s_t.index.max()

    emissions_start = s_t[year_start]
    emissions_end = s_t[year_end]

    l_lin = line(
        x1=year_start,
        y1=emissions_start,
        x2=year_end,
        y2=emissions_end,
        xrange_start=year_start,
        xrange_end=2250,
        xindexname="year",
    )
    l_lin.name = "trend_lin_kt"
    l_lin.clip(lower=0, inplace=True)

    l_const = line(
        x1=year_start,
        y1=emissions_end,
        x2=year_end,
        y2=emissions_end,
        xrange_start=year_start,
        xrange_end=2250,
        xindexname="year",
    )
    l_const.name = "trend_const_kt"

    df = df.join(l_lin, how="outer")
    df = df.join(l_const, how="outer")

    return df


def add_trend_continuation(df):
    assert "co2_kt_total" in df.columns
    assert "trend_const_kt" in df.columns
    assert "trend_lin_kt" in df.columns

    df["measured_n_trendlin_kt"] = df["co2_kt_total"]
    df["measured_n_trendconst_kt"] = df["co2_kt_total"]

    df["measured_n_trendlin_kt"].fillna(df["trend_lin_kt"], inplace=True)
    df["measured_n_trendconst_kt"].fillna(df["trend_const_kt"], inplace=True)

    return df


# def compute_trend(df_emissions):

#     df_e = df_emissions.sum(axis=1)

#     year_max = df_e.index.max()
#     year_start = 2014
#     assert 2014 in df_e.index

#     e_max = df_e[year_max]
#     e_start = df_e[year_start]

#     t = LinTrend(year_start, e_start, year_max, e_max)

#     return