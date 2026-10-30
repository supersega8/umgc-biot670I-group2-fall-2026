# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:49:04 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path


fips_dict=state_fips = {
    "Alabama": 1,
    "Alaska": 2,
    "Arizona": 4,
    "Arkansas": 5,
    "California": 6,
    "Colorado": 8,
    "Connecticut": 9,
    "Delaware": 10,
    "Florida": 12,
    "Georgia": 13,
    "Hawaii": 15,
    "Idaho": 16,
    "Illinois": 17,
    "Indiana": 18,
    "Iowa": 19,
    "Kansas": 20,
    "Kentucky": 21,
    "Louisiana": 22,
    "Maine": 23,
    "Maryland": 24,
    "Massachusetts": 25,
    "Michigan": 26,
    "Minnesota": 27,
    "Mississippi": 28,
    "Missouri": 29,
    "Montana": 30,
    "Nebraska": 31,
    "Nevada": 32,
    "New Hampshire": 33,
    "New Jersey": 34,
    "New Mexico": 35,
    "New York": 36,
    "North Carolina": 37,
    "North Dakota": 38,
    "Ohio": 39,
    "Oklahoma": 40,
    "Oregon": 41,
    "Pennsylvania": 42,
    "Rhode Island": 44,
    "South Carolina": 45,
    "South Dakota": 46,
    "Tennessee": 47,
    "Texas": 48,
    "Utah": 49,
    "Vermont": 50,
    "Virginia": 51,
    "Washington": 53,
    "West Virginia": 54,
    "Wisconsin": 55,
    "Wyoming": 56
}

fips_dict_short = {
    'al': 1,
    'ak': 2,
    'az': 4,
    'ar': 5,
    'ca': 6,
    'co': 8,
    'ct': 9,
    'de': 10,
    'fl': 12,
    'ga': 13,
    'hi': 15,
    'id': 16,
    'il': 17,
    'in': 18,
    'ia': 19,
    'ks': 20,
    'ky': 21,
    'la': 22,
    'me': 23,
    'md': 24,
    'ma': 25,
    'mi': 26,
    'mn': 27,
    'ms': 28,
    'mo': 29,
    'mt': 30,
    'ne': 31,
    'nv': 32,
    'nh': 33,
    'nj': 34,
    'nm': 35,
    'ny': 36,
    'nc': 37,
    'nd': 38,
    'oh': 39,
    'ok': 40,
    'or': 41,
    'pa': 42,
    'ri': 44,
    'sc': 45,
    'sd': 46,
    'tn': 47,
    'tx': 48,
    'ut': 49,
    'vt': 50,
    'va': 51,
    'wa': 53,
    'wv': 54,
    'wi': 55,
    'wy': 56
}
filepath=Path(input(r"Tell me the filepath of the final merged 1995-2024.csv for each disease, not including the actual csv file yet: "))

popfilepath=Path(input(r"Tell me where the historical population csv (historical_state_population_by_year.csv) is stored, not including the actual csv file yet: "))

savepath=Path(input(r"Tell me where you would like the merged population/measles csv saved?: "))

diseases=['measles','mumps','rubella']

for disease in diseases:
    df=pd.read_csv(filepath / fr"1995-2026_{disease}.csv")
    
    popdf=pd.read_csv(popfilepath / r"historical_state_population_by_year.csv")
    popdf = popdf.map(lambda x: x.lower() if isinstance(x, str) else x)
    
    list(popdf)
    
    
    popdf['FIPS_CODE']=popdf['STATE'].map(fips_dict_short)
    
    
    
    
    
    
    lowercase_dict={key.lower(): value for key,value in fips_dict.items()}
    
    
    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
    
    df['FIPS_CODE']=df['Reporting_Area'].map(lowercase_dict)
    
    df = df.dropna(subset=['FIPS_CODE'])
    
    df['FIPS_CODE'] = df['FIPS_CODE'].astype(int)
    
    mergeddf = df.merge(
        popdf[["YEAR", "FIPS_CODE", "POPULATION"]],
        on=["YEAR", "FIPS_CODE"],
        how="left",
    )
    
    mergeddf['POPULATION']=mergeddf['POPULATION'].astype('Int64')
    
    if disease=='measles':
        
        
    
        mergeddf['indigenous']=mergeddf['indigenous'].astype('Int64')
        mergeddf['imported']=mergeddf['imported'].astype('Int64')
        
        mergeddf['DISEASE_INCIDENCE']=(mergeddf['indigenous']+mergeddf['imported'])/(mergeddf['POPULATION'])*100000
        mergeddf.to_csv(savepath / fr"1995-2026_{disease}_pop.csv",index=False)
              
        df.to_csv(savepath / fr"1995-2026_{disease}_fips.csv")
    else:
    
        mergeddf[f'{disease}']=mergeddf[f'{disease}'].astype('Int64')
        
        
        
        mergeddf['DISEASE_INCIDENCE']=(mergeddf[f'{disease}'])/(mergeddf['POPULATION'])*100000
        
        mergeddf.to_csv(savepath / fr"1995-2026_{disease}_pop.csv",index=False)
              
        df.to_csv(savepath / fr"1995-2026_{disease}_fips.csv")
       
     