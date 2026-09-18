# tycho_filter_columns.py

# @author: Natasha

# filter Project Tycho data to focus on disease column = measles, mumps, polio, or rubella
import pandas as pd

# use correct file name/path for device
df = pd.read_csv(
    'Project_Tycho_®_Level_1_Data_20260831.csv', 
    dtype={'cases': float}, 
    na_values=['\\N']
)

target_values = ['MEASLES', 'MUMPS', 'POLIO', 'RUBELLA']

filtered_df = df[df['disease'].isin(target_values)]
  
filtered_df.to_csv('Project Tycho Filtered.csv', index=False)

# parse epiweek column into year and week information
# epiweek column example: 192801 = year 1928 week 1

import pandas as pd
from epiweeks import Week
# install epiweeks as needed

df = pd.read_csv('Project Tycho Filtered.csv')

df['epiweek_str'] = df['epi_week'].astype(str)
df['Week_Obj'] = df['epiweek_str'].apply(lambda x:Week.fromstring(x))
df['Year'] = df['Week_Obj'].apply(lambda w: w.year)
df['Week'] = df['Week_Obj'].apply(lambda w: w.week)

df['Week_End_Date'] = pd.to_datetime(df['Week_Obj'].apply(lambda w: w.enddate()))
df['Month'] = df['Week_End_Date'].dt.month

df = df.drop(columns=['epiweek_str', 'Week_Obj', 'Week_End_Date'])
df.to_csv('Project Tycho Filtered Dates.csv', index=False)
