# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 02:35:10 2026

@author: sumit
"""

from data_analyzer import dataanalyzer
import pyreadr as py
from pathlib import Path

#creating the indexes for the currently availabe R files (2006-2024, except for 2015 since no R files found for that year)

indexstring = "95,96,97,98,99,00,01,02,03,04,05,15"
index=indexstring.split(",")
#running it here, basically importing the modules 


analyzer = dataanalyzer(
        rdata_folder=
        input(r"Tell me the files where the R data should be stored: "),
    
        dat_folder=
        "",
    
        r_folder=
        ""
    )
if __name__ == "__main__":
    csv_folder = Path(input(r"Tell me where you want to save the CSV?: "))
    for number in index:
        rdata_file=analyzer.rdata_folder /f"NISPUF{number}.RData"
        result=py.read_r(rdata_file)
        print(result.keys())
        df=result["data_read"]
        csv_file = csv_folder / f"NISPUF{number}.csv"
    
        df.to_csv(csv_file, index=False)
    
        print(f"Saved {csv_file}")