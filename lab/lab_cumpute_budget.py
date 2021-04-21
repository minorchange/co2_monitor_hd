start_budget_2020 = 13009.5


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import read_emissions

df_all = read_emissions()

df_measured_since_20200101 = df_all[df_all.index >=2020]
measured_co2kt_since20200101 = df_measured_since_20200101.sum().sum()


last_measured_year = df_all.index.max() 

latest_emissions_ktperyear = df_all.loc[df_all.index.max()].sum()
assert latest_emissions_ktperyear > -1
assert latest_emissions_ktperyear < 3000

seconds_per_year = 60*60*24*365.25
latest_emissions_ktpersecond = latest_emissions_ktperyear / seconds_per_year

import datetime

last_measured_year_since_2019 = max(last_measured_year, 2019)
last_measured_second = datetime.datetime.strptime(f'{last_measured_year_since_2019}-12-31 23:59:59', '%Y-%m-%d %H:%M:%S')

print(last_measured_second)
now = datetime.datetime.now() 
seconds_since_last_measured_second = (now - last_measured_second).total_seconds()


estimated_emissions_kt = latest_emissions_ktpersecond * seconds_since_last_measured_second
total_emissions_kt = measured_co2kt_since20200101 + estimated_emissions_kt


print(total_emissions_kt)
print()

remaining_budget = start_budget_2020 - total_emissions_kt
remaining_seconds = remaining_budget / latest_emissions_ktpersecond

from dateutil.relativedelta import relativedelta
year_when_budget_is_depletet = (now + relativedelta(seconds=+remaining_seconds)).year


print(year_when_budget_is_depletet)

