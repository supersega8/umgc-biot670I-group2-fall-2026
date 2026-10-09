# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 00:14:19 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path


yearstr="95,96,97,98,99,00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24"

yearsindex=yearstr.split(',')





cleaned_path=Path(input(r"Please tell me the file path where you saved the cleaned NIS data to combine them into one big CSV: "))

csv_list = list(cleaned_path.glob("*.csv"))

df_list=[]

for year in yearsindex:
    
    for file in csv_list:
        filestr=str(file)
        if filestr.endswith(f"{year}.csv"):
            df=pd.read_csv(file)
            df_list.append(df)
        else:
            continue

for i,df in enumerate(df_list):
    print(f"Dataframe index {i}")
 
combineddf=pd.concat(df_list,ignore_index=True)
combineddf.to_csv(cleaned_path / "combined.csv",index=False)   

