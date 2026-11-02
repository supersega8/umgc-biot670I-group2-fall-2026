# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:07:05 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path

filepath=Path(input(r"Tell me where the 2016-2023_mumpsandrubella.csv is, don't include the actual csv yet"))

df=pd.read_csv(filepath / r"2016-2023_mumpsandrubella.csv")

df=df.map(lambda x:x.lower() if isinstance(x,str) else x)

sorted_df=df.sort_values(by=['Disease','Year'])



final_df=sorted_df.pivot_table(
    index=['Regions/States','Year'],
    columns='Disease',
    values='Case Count',
    aggfunc='first'
    ).reset_index()

final_df.to_csv(filepath / r"2016-2023_mumpsandrubella_transformed.csv")