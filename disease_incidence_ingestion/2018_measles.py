# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 18:48:32 2026

@author: sumit
"""

import pandas as pd

import re

from pathlib import Path


befores = []
afters = []
  
measlesgroup = []

filepath=Path(input(r"Tell me the filepath for the 2018.txt, without including it yet"))

filepath2018=filepath / r"2018.txt"
with filepath2018.open() as file:
    for line in (l.lower() for l in file):
        newline = re.sub(r"_{1,3}|[-–——]|[â€”""]", "0", line)
        pattern1= r"[a-zA-Z]+\."
        pattern2 = r"[a-zA-Z]+"
        pattern3 = r"\b\d{1,3}(?:,\d{3})*\b"
        
        

        
        patternlist=[pattern1,pattern2]
        
        for pattern in patternlist:
            match = re.search(pattern, line)
            if match:
                numbermatch=re.search(pattern3,line)
                if numbermatch:
                    start, finish = numbermatch.span()

                    before = newline[:start].strip()
                    after = newline[start:].strip()
                    
                    befores.append(before)
                    afters.append(after)
                    matches = list(re.finditer(pattern3, after))
                    last_3_matches = matches[-3:]
                    cleaned_parts = [re.sub(r"\s", "0", m.group()) for m in last_3_matches]
                    measles = ",".join(cleaned_parts)
                    measlesgroup.append(measles)
                        
                    break

                for i, item in enumerate(afters):
                     print(f"Index {i}: {item}")
                afterdf=pd.DataFrame()
                afterdf['measles_firstrun']=afters
                afterdf['YEAR']=2018
                cols=list(afterdf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                afterdf=afterdf[cols]
                afterdf.to_csv(filepath / r"csv\after\2018.csv",index=False)
                
                for i, item in enumerate(befores):
                    print(f"Index {i}: {item}")
                beforedf=pd.DataFrame()
                beforedf['states']=befores
                beforedf['YEAR']=2018
                cols=list(beforedf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                beforedf=beforedf[cols]
                beforedf.to_csv(filepath / r"csv\before\2018.csv",index=False)
                for i, item in enumerate(measlesgroup):
                     print(f"Measles {i}: {item}")
                measlesdf=pd.DataFrame()
                measlesdf['measles']=measlesgroup
             
                 
                measlesdf['YEAR']=2018
                cols=list(measlesdf.columns)
                
                measlesdf=measlesdf[cols]
                measlesdf.to_csv(filepath / r"csv\measles\2018.csv",index=False)   