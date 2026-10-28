# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 23:25:50 2026

@author: sumit
"""

import pandas as pd
from scipy.stats import spearmanr,pearsonr
from pathlib import Path

#This script makes an initial overall analysis csv for each disease type. 
#Spearman and Pearson coefficients are used to compare the analysis 


filepath=Path(input(r"Tell me the filepath to the final merged csvs for each disease type,  do not include the actual csvs yet:  "))

savepath=Path(input("tell me where you would like to save the processed csv's after analysis?"))

measlesdf=pd.read_csv(filepath / "1995-2024_measles_merged.csv")

measlesdf['DISEASE']='MEASLES'

mumpsdf=pd.read_csv(filepath / r"1995-2024_mumps_merged.csv")

mumpsdf['DISEASE']='MUMPS'

rubelladf=pd.read_csv(filepath / r"1995-2024_rubella_merged.csv")

rubelladf['DISEASE']='RUBELLA'

mmr_df=pd.concat([measlesdf,mumpsdf,rubelladf],ignore_index=True)

mmr_df[['DISEASE','rubella']]=mmr_df[['rubella','DISEASE']]

mmr_df_rename=mmr_df.rename(columns={'DISEASE':'rubella','rubella':'DISEASE'})

mmr_df_rename.to_csv(filepath / r"mmr_combined.csv",index=False)


resultsmeasles = []
resultsmumps=[]

resultsrubella=[]
measlesdf = measlesdf.sort_values(['FIPS_CODE', 'YEAR'])

mumpsdf=mumpsdf.sort_values(['FIPS_CODE','YEAR'])

rubelladf=rubelladf.sort_values(['FIPS_CODE','YEAR'])







for yr, group in measlesdf.groupby('YEAR'):

    spearman_measles = spearmanr(group['DISEASE_INCIDENCE'], group['STATE_WEIGHTED'])
    pearson_measles = pearsonr(group['DISEASE_INCIDENCE'], group['STATE_WEIGHTED'])

    resultsmeasles.append({
        'YEAR': yr,
        'spearman-correlation': spearman_measles.statistic,
        'spearman-pvalue': spearman_measles.pvalue,
        'pearson-correlation': pearson_measles.statistic,
        'pearson-pvalue': pearson_measles.pvalue,
    })

resultsmeaslesdf = pd.DataFrame(resultsmeasles)

resultsmeaslesdf.to_csv(savepath / r"overall_analysis_measles.csv",index=False)

for yr, group in mumpsdf.groupby('YEAR'):
    valid=group[['DISEASE_INCIDENCE','STATE_WEIGHTED']].dropna()
    spearman_mumps = spearmanr(valid['DISEASE_INCIDENCE'],valid['STATE_WEIGHTED'])
    pearson_mumps = pearsonr(valid['DISEASE_INCIDENCE'],valid['STATE_WEIGHTED'])

    resultsmumps.append({
        'YEAR': yr,
        'spearman-correlation': spearman_mumps.statistic,
        'spearman-pvalue': spearman_mumps.pvalue,
        'pearson-correlation': pearson_mumps.statistic,
        'pearson-pvalue': pearson_mumps.pvalue,
    })

resultsmumpsdf = pd.DataFrame(resultsmumps)

resultsmumpsdf.to_csv(savepath / r"overall_analysis_mumps.csv",index=False)

for yr, group in rubelladf.groupby('YEAR'):
    valid=group[['DISEASE_INCIDENCE','STATE_WEIGHTED']].dropna()
    spearman_rubella = spearmanr(valid['DISEASE_INCIDENCE'],valid['STATE_WEIGHTED'])
    pearson_rubella = pearsonr(valid['DISEASE_INCIDENCE'],valid['STATE_WEIGHTED'])

    resultsrubella.append({
        'YEAR': yr,
        'spearman-correlation': spearman_rubella.statistic,
        'spearman-pvalue': spearman_rubella.pvalue,
        'pearson-correlation': pearson_rubella.statistic,
        'pearson-pvalue': pearson_rubella.pvalue,
    })

resultsrubelladf = pd.DataFrame(resultsrubella)

resultsrubelladf.to_csv(savepath / r"overall_analysis_rubella.csv",index=False)
