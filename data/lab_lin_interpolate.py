import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def linear_interpolation(data_points):
    years, values = zip(*data_points.items())
    years = np.array(years)
    values = np.array(values)

    # Create the interpolation function
    interpolation_function = np.poly1d(np.polyfit(years, values, 1))

    # Generate years for interpolation
    interpolated_years = np.arange(years[0], years[-1] + 1)

    # Interpolate values for the generated years
    interpolated_values = interpolation_function(interpolated_years)

    # Create a dictionary with interpolated time series
    interpolated_time_series = {
        year: value for year, value in zip(interpolated_years, interpolated_values)
    }

    return interpolated_time_series


# Example usage
data_points = {2020: 900, 2030: 850, 2040: 404}
result = linear_interpolation(data_points)

# Print the result
print(result)
df = pd.Series(result)
print()
