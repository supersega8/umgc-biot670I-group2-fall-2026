# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:17:59 2026

@author: sumit
"""



import pandas as pd
from pathlib import Path


#combining all the csv's that were produced from the 2003-2015 regex cleaners to make a combined csv 
combineddfinput=Path(input(r"Tell me the filepath for the disease_incidence\csv filepath is, don't include the actual csv's yet: "))

df=pd.read_csv(combineddfinput / r"measles\combined.csv")

column_list=df.columns.tolist()

print(column_list)


df[['indigenous','imported']]=df['measles'].str.split(',',n=1,expand=True).copy()

mumpscombined=pd.read_csv(combineddfinput / r"mumps\combined.csv")

rubellacombined=pd.read_csv(combineddfinput/ r"rubella\combined.csv")

df['mumps']=mumpscombined['mumps']
df['rubella']=rubellacombined['rubella']
df.to_csv(combineddfinput /r"csv\combinedsplit.csv")