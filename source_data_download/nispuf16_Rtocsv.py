# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 23:13:18 2026

@author: sumit
"""
import pyreadr as py
import pandas as pd
from pathlib import Path

inputfilepath=input("Tell me the input R file path: ")
resultfilepath=input("Tell me the output path where the csv will be stored: ")
edition="NISPUF16"

file=Path(rf"{inputfilepath}\{edition}.RData")
resultpath=Path(rf"{resultfilepath}\{edition}.csv")
result=py.read_r(file)

print(result.keys())

df=result['NISPUF16']

df.to_csv(resultpath,index=False)