# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:45:08 2026

@author: sumit
"""

import pandas as pd
from pathlib import Path




def csvtodf20192021(*args):
    for item in args:
        filedirectory = Path(
           input(r"Tell me the input filepath for the 2019-2021 measles csv files: ")
        )
        if item=='2019':
            df=pd.read_csv(filedirectory / r"2020.csv")   
        else:
            
            df=pd.read_csv(filedirectory / f"{item}.csv")
        
        



        df[f'Measles, Imported, Cum {item}'] = pd.to_numeric(
            df[f'Measles, Imported, Cum {item}'].astype(str).str.replace(',', ''),
            errors='coerce'
        )
        df[f'Measles, Indigenous, Cum {item}'] = pd.to_numeric(
            df[f'Measles, Indigenous, Cum {item}'].astype(str).str.replace(',', ''),
            errors='coerce'
        )



        sorted_df = df.sort_values(
            by=['Reporting Area', 'MMWR Week'],
            ascending=[True, True]
        )

        final_df = sorted_df.groupby(
            ['Reporting Area', 'MMWR Year'],
            as_index=False
        ).agg({
         
            f'Measles, Imported, Cum {item}':'max',
            f'Measles, Indigenous, Cum {item}':'max'
            
        }).fillna(0)
        
        final_df.to_csv(fr"C:\Users\sumit\Documents\UMGC 670 Fall 2026 capstone\disease_incidence\{item}_transformed.csv",index=False)       
        print(final_df)
        
    combinedf=pd.concat([pd.read_csv(fr"C:\Users\sumit\Documents\UMGC 670 Fall 2026 capstone\disease_incidence\{item}_transformed.csv") for item in args], ignore_index=True)
    combinedf.to_csv(r"C:\Users\sumit\Documents\UMGC 670 Fall 2026 capstone\disease_incidence\combined_2019-2021_transformed.csv",index=False)       
    

csvtodf20192021('2019','2020','2021')