# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 21:21:57 2026

@author: sumit
"""

import pandas as pd
from scipy.stats import spearmanr,pearsonr
from pathlib import Path



filepath=Path(input(r"Tell me the filepath to the final merged csvs for each disease type,  do not include the actual csvs yet:  "))

savepath=Path(input("tell me where you would like to save the processed csv's after analysis?"))


mmr_df_rename=pd.read_csv(filepath / "mmr_combined.csv")




year_index=[1,2,3]

years=['one','two','three']

diseases = ['MEASLES', 'MUMPS', 'RUBELLA']

for disease in diseases:

    disease_df = mmr_df_rename[
        mmr_df_rename['DISEASE'] == disease
    ].copy()

    disease_df = disease_df.sort_values(['FIPS_CODE', 'YEAR'])

    for year, item in zip(year_index, years):

        results2 = []

        disease_df['LAG_1'] = (
            disease_df.groupby('FIPS_CODE')['STATE_WEIGHTED'].shift(year)
        )

        previous_year = (
            disease_df.groupby('FIPS_CODE')['YEAR'].shift(year)
        )

        disease_df.loc[
            
            disease_df['YEAR'] - previous_year != year, 'LAG_1'
        ] = float('nan')

        for yr, group in disease_df.groupby('YEAR'):

            valid = group[['DISEASE_INCIDENCE', 'LAG_1']].dropna()

            if len(valid) < 3:
                continue

            if valid['DISEASE_INCIDENCE'].nunique() < 2 or valid['LAG_1'].nunique() < 2:
                continue

            spearman = spearmanr(valid['DISEASE_INCIDENCE'], valid['LAG_1'])
            pearson = pearsonr(valid['DISEASE_INCIDENCE'], valid['LAG_1'])

            results2.append({
                'DISEASE':disease,
                'YEAR': yr,
                'N': len(valid),
                'spearman-correlation': spearman.statistic,
                'spearman-pvalue': spearman.pvalue,
                'pearson-correlation': pearson.statistic,
                'pearson-pvalue': pearson.pvalue
            })

        results2df = pd.DataFrame(results2)
        
        results2df.to_csv(
            savepath / fr"{disease}_{item}_yearlag.csv",
            index=False
        )
