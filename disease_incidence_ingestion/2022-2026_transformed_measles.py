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

df = pd.read_csv(filedirectory / "2022-2026_measles.csv")

df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

df['Cumulative YTD Current MMWR Year'] = pd.to_numeric(
    df['Cumulative YTD Current MMWR Year']
    .astype(str)
    .str.replace(',', ''),
    errors='coerce'
)


df = df[df['Label'].str.contains('measles', na=False)].copy()


df['case_type'] = df['Label'].str.extract(
    r'(indigenous|imported)', expand=False
)

df = df.dropna(subset=['case_type'])

final_df = (
    df.groupby(
        ['Reporting Area', 'Current MMWR Year', 'case_type'],
        as_index=False
    )
    .agg({
        'Cumulative YTD Current MMWR Year': 'max'
    })
)

final_df['Cumulative YTD Current MMWR Year'] = (
    final_df['Cumulative YTD Current MMWR Year'].fillna(0)
)


final_df = final_df.pivot(
    index=['Reporting Area', 'Current MMWR Year'],
    columns='case_type',
    values='Cumulative YTD Current MMWR Year'
).reset_index()

final_df.columns.name = None

final_df[['indigenous', 'imported']] = (
    final_df[['indigenous', 'imported']].fillna(0)
)

final_df = final_df.rename(columns={
    'Current MMWR Year': 'YEAR'
})

final_df.to_csv(
    filedirectory / "2022-2026_transformed_measles.csv",
    index=False
)