# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 22:04:36 2026

@author: sumit
"""

import pandas as pd
from scipy.stats import spearmanr,pearsonr
from pathlib import Path




filepath=Path(input(r"Tell me the filepath to the final combined (mmr_combined.csv) do not include the actual csv yet:  "))

savepath=Path(input("tell me where you would like to save the processed csv's after analyis?"))

df = pd.read_csv(filepath / "mmr_combined.csv")

diseases = ['MEASLES', 'MUMPS', 'RUBELLA']

years = ['one', 'two', 'three']
year_index = [1, 2, 3]

all_results = {}

for disease in diseases:

    disease_results = []

    statesdf = df[df['DISEASE'] == disease].copy()

    statesdf = statesdf.sort_values(['FIPS_CODE', 'YEAR'])

    statesdf['COVERAGE_CHANGE'] = (
        statesdf.groupby('FIPS_CODE')['STATE_WEIGHTED'].diff()
    )

    statesdf['INCIDENCE_CHANGE'] = (
        statesdf.groupby('FIPS_CODE')['DISEASE_INCIDENCE'].diff()
    )

    
    year_gap = statesdf.groupby('FIPS_CODE')['YEAR'].diff()

    statesdf.loc[
        year_gap != 1,
        ['COVERAGE_CHANGE', 'INCIDENCE_CHANGE']
    ] = float('nan')

    for year, item in zip(year_index, years):

        results2 = []

        statesdf['LAG_1'] = (
            statesdf.groupby('FIPS_CODE')['COVERAGE_CHANGE'].shift(year)
        )

        previous_year = (
            statesdf.groupby('FIPS_CODE')['YEAR'].shift(year)
        )

        # Validate the calendar-year lag
        statesdf.loc[
            statesdf['YEAR'] - previous_year != year,
            'LAG_1'
        ] = float('nan')

        for state, group in statesdf.groupby('FIPS_CODE'):

            valid = group[
                ['LAG_1', 'INCIDENCE_CHANGE']
            ].dropna()

            result = {
                'FIPS_CODE': state,
                'N': len(valid),
                'spearman-correlation': float('nan'),
                'spearman-pvalue': float('nan'),
                'pearson-correlation': float('nan'),
                'pearson-pvalue': float('nan'),
                'TIME_LAG': year
            }

            if (len(valid) >= 3 and
                valid['LAG_1'].nunique() >= 2 and
                valid['INCIDENCE_CHANGE'].nunique() >= 2):

                spearman = spearmanr(
                    valid['LAG_1'],
                    valid['INCIDENCE_CHANGE']
                )

                pearson = pearsonr(
                    valid['LAG_1'],
                    valid['INCIDENCE_CHANGE']
                )

                result.update({
                    'DISEASE':disease,
                    'spearman-correlation': spearman.statistic,
                    'spearman-pvalue': spearman.pvalue,
                    'pearson-correlation': pearson.statistic,
                    'pearson-pvalue': pearson.pvalue
                })

            results2.append(result)

        results2df = pd.DataFrame(results2)
        

     
        

        results2df.to_csv(
            savepath / fr"{disease}_{item}_yearlag_state_analysis.csv",
            index=False
        )

        disease_results.append(results2df)

    all_results[disease] = pd.concat(
        disease_results, ignore_index=True
    )

    all_results[disease].to_csv(
        savepath / fr"states_analysis_{disease}.csv",
        index=False
    )
