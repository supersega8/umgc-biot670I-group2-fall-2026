# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 21:06:55 2026

@author: sumit
"""

from pypdf import PdfReader
from pathlib import Path
import re
import pandas as pd


filedirectory = Path(input(r"Tell me the filepath with the 2003-2015 pdf files, don't include the actual pdfs yet: ")

).mkdir(parents=True, exist_ok=True)

savepath=Path(input(r"Tell me where the csv files should be saved: ")).mkdir(parents=True, exist_ok=True)

pdf_list = list(filedirectory.glob("*.pdf"))


years = [
    '2003','2004','2005','2006','2007','2008','2009',
    '2010','2011','2012','2013','2014','2015'
]

measles_index = [
    (2,3),(2,3),(0,1),(0,1),(0,1),(1,2),(1,2),
    (5,6),(5,6),(1,2),(1,2),(5,6),(2,3)
]


def measlescleanerpdf(filedirectory,pdf_list,years,measles_index):


    for file in pdf_list:
    
        for yearposition, year in enumerate(years):
    
            if str(file).endswith(f"{year}.pdf"):
    
                read = PdfReader(file)
                print(f"Processing {year}: ")
    
                befores = []
                afters = []
                
                measlesgroup = []
    
                for page in read.pages:
    
                    text = page.extract_text()
                    lowertext = text.lower()
    
                    if "table 2" in lowertext and "measles" in lowertext:
    
                        for line in lowertext.splitlines():
    
                            newline = re.sub(r"_{1,3}|[-–—]", "0", line)
    
                            pattern1 = r"[a-zA-Z]+\."
                            pattern2 = r"[a-zA-Z]+"
                            pattern4 = r"\b\d{1,3}(?:,\d{3})*\b"
    
                            patternlist = [pattern1, pattern2]
    
                            for pattern in patternlist:
    
                                match = re.search(pattern, newline)
    
                                if match:
    
                                    numbermatch = re.search(pattern4, newline)
    
                                    if numbermatch:
    
                                        start, finish = numbermatch.span()
    
                                        before = newline[:start].strip()
                                        after = newline[start:].strip()
                                        befores.append(before)
                                        afters.append(after)
                                        matches = list(re.finditer(pattern4, after))
    
                                        beginning = measles_index[yearposition][0]
                                        end = measles_index[yearposition][1]
    
                                        if len(matches) > end:
    
                                            measles = (
                                                matches[beginning].group()
                                                + ','
                                                + matches[end].group()
                                                )
    
                                            measlesgroup.append(measles)
    
    
                                        break
    
              
    
                for i, item in enumerate(afters):
                    print(f"Index {i}: {item}")
                afterdf=pd.DataFrame()
                afterdf['measles_firstrun']=afters
                afterdf['YEAR']=year
                cols=list(afterdf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                afterdf=afterdf[cols]
                afterdf.to_csv(filedirectory / rf"csv\after\{year}.csv",index=False).mkdir(parents=True, exist_ok=True)
    
                for i, item in enumerate(befores):
                    print(f"Index {i}: {item}")
                beforedf=pd.DataFrame()
                beforedf['states']=befores
                beforedf['YEAR']=year
                cols=list(beforedf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                beforedf=beforedf[cols]
                beforedf.to_csv(filedirectory / rf"csv\before\{year}.csv",index=False).mkdir(parents=True, exist_ok=True)
                for i, item in enumerate(measlesgroup):
                    print(f"Measles {i}: {item}")
                measlesdf=pd.DataFrame()
                measlesdf['measles']=measlesgroup
                
                measlesdf['YEAR']=year
                cols=list(measlesdf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                measlesdf=measlesdf[cols]
                measlesdf.to_csv(filedirectory / rf"csv\measles\{year}.csv",index=False).mkdir(parents=True, exist_ok=True)   
                
    
    group=['after','before','measles']
    
    
    
    
    
    for member in group:
        dataframecsvfiles=Path(savepath / fr"\csv\{member}").mkdir(parents=True, exist_ok=True)
        csv_list = list(dataframecsvfiles.glob("*.csv"))
        combineddf=pd.concat((pd.read_csv(file) for file in csv_list),ignore_index=True)
        combineddf.to_csv(dataframecsvfiles / fr"csv\{member}\combined.csv",index=False).mkdir(parents=True, exist_ok=True)     



