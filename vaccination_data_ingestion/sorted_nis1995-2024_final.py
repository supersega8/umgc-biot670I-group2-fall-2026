# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 20:24:47 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path


cleaned_combined_filepath = Path(input(r"Tell me where the combined_1995-2024_cleaned csv filepath is: ")    
)

df = pd.read_csv(
    cleaned_combined_filepath / "combined_1995-2024_cleaned.csv"
).copy()

sorted_df = df.sort_values(
    by=['YEAR', 'FIPS_CODE'],
    ascending=[True, True]
)

sorted_df['MMR_PLUS1'] = (
    sorted_df['P_NUMMMX'] >= 1
).astype('Int64')

sorted_df['WEIGHTED_MMR'] = (
    sorted_df['MMR_PLUS1'] * sorted_df['PROVWT']
)

sorted_df['STATE_WEIGHTED'] = (
    sorted_df.groupby(['YEAR', 'FIPS_CODE'])['WEIGHTED_MMR'].transform('sum')
    /
    sorted_df.groupby(['YEAR', 'FIPS_CODE'])['PROVWT'].transform('sum')
) * 100

sorted_df = sorted_df.drop(columns=['MMR_PLUS1'])

state_df=sorted_df.copy()

state_df = sorted_df[
    ['YEAR', 'FIPS_CODE','state_name', 'STATE_WEIGHTED']
].drop_duplicates(
    subset=['YEAR', 'FIPS_CODE']
)

state_df.to_csv(
    cleaned_combined_filepath / "sorted_combined_cleaned.csv",
    index=False
)


