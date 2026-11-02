# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:16:08 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path




filedirectory = Path(
    r"C:\Users\sumit\Documents\UMGC 670 Fall 2026 capstone\disease_incidence"
).mkdir(parents=True, exist_ok=True)

df = pd.read_csv(filedirectory / r"2022-2026_rubella.csv")

df=df.map(lambda x:x.lower() if isinstance(x,str) else x)

df['Cumulative YTD Current MMWR Year'] = pd.to_numeric(
    df['Cumulative YTD Current MMWR Year'].astype(str).str.replace(',', ''),
    errors='coerce'
)

df=df[df['Label'] != 'rubella, congenital syndrome']




sorted_df = df.sort_values(
    by=['Reporting Area', 'Current MMWR Year', 'MMWR WEEK', 'Label']
)

final_df = (
    sorted_df
    .groupby(
        ['Reporting Area', 'Current MMWR Year', 'Label'],
        as_index=False
    )
    .agg({
        'Current week': 'sum',
        'Cumulative YTD Current MMWR Year': 'max'
    })
).fillna(0)


final_df = final_df.pivot_table(
    index=['Reporting Area', 'Current MMWR Year','Label'],
    columns=None,
    values=['Cumulative YTD Current MMWR Year'],
    aggfunc='first'
).reset_index()





final_df.to_csv(r"C:\Users\sumit\Documents\UMGC 670 Fall 2026 capstone\disease_incidence\2022-2026_transformed_rubella.csv",index=False)