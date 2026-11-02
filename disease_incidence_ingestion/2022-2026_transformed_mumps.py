# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:16:08 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path




filedirectory = Path(
    r"C:\Users\sumit\Documents\UMGC 670 Fall 2026 capstone\disease_incidence"
)

df = pd.read_csv(filedirectory / "2022-2026_rubella.csv")

df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

df['Cumulative YTD Current MMWR Year'] = pd.to_numeric(
    df['Cumulative YTD Current MMWR Year']
    .astype(str)
    .str.replace(',', ''),
    errors='coerce'
)

final_df = (
    df.groupby(
        ['Reporting Area', 'Current MMWR Year', 'Label'],
        as_index=False
    )
    .agg({
        'Cumulative YTD Current MMWR Year': 'max'
    })
)

final_df['Cumulative YTD Current MMWR Year'] = (
    final_df['Cumulative YTD Current MMWR Year'].fillna(0)
)

final_df.to_csv(
    filedirectory / "2022-2026_transformed_rubella.csv",
    index=False
)