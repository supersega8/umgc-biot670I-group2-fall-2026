# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 23:45:59 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path


filepath=Path(input(r"Tell me the file path of the final _pop.csv file for each disease, do not include the actual csv file yet: "))

savepath=Path(input("tell me where you would like to save the processed csv's after analyis?"))

df=pd.read_csv(filepath / r"1995-2026_measles_pop.csv")

df2=pd.read_csv(filepath / r"1995-2026_mumps_pop.csv")

df3=pd.read_csv(filepath / r"1995-2026_rubella_pop.csv")

vaxdf=pd.read_csv(filepath / r"sorted_combined_cleaned.csv")

df['YEAR']=df['YEAR'].astype('int64')

mergeddf1 = df.merge(
    vaxdf[["YEAR", "FIPS_CODE", "STATE_WEIGHTED"]],
    on=["YEAR", "FIPS_CODE"],
    how="inner",
)

mergeddf2 = df2.merge(
    vaxdf[["YEAR", "FIPS_CODE", "STATE_WEIGHTED"]],
    on=["YEAR", "FIPS_CODE"],
    how="inner",
)

mergeddf3 = df3.merge(
    vaxdf[["YEAR", "FIPS_CODE", "STATE_WEIGHTED"]],
    on=["YEAR", "FIPS_CODE"],
    how="inner",
)

mergeddf1.to_csv(savepath / r"1995-2024_measles_merged.csv",index=False)

mergeddf2.to_csv(savepath / r"1995-2024_mumps_merged.csv",index=False)

mergeddf3.to_csv(savepath / r"1995-2024_rubella_merged.csv",index=False)


