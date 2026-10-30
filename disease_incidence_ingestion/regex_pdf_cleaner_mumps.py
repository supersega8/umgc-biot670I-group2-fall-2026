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



mumps_index=[5,5,0,0,0,0,8,5,5,0,0,5,0]

str_mumps=[str(num) for num in mumps_index]


def mumpscleanerpdf(filedirectory,pdf_list,years,mumps_index):


    for file in pdf_list:
    
        for yearposition, year in enumerate(years):
    
            if str(file).endswith(f"{year}.pdf"):
    
                read = PdfReader(file)
                print(f"Processing {year}: ")
    
                befores = []
                afters = []
                
                mumpsgroup= []
                
    
                for page in read.pages:
    
                    text = page.extract_text()
                    lowertext = text.lower()
    
                    if "table 2" in lowertext and "mumps" in lowertext:
    
                        for line in lowertext.splitlines():
    
                            newline = re.sub(r"_{1,3}|[-–—]", "0", line)
    
                            pattern1 = r"[a-zA-Z]+\."
                            pattern2 = r"[a-zA-Z]+"
                            pattern3 = r"\b\d{1,3}(?:,\d{3})*\b"
    
                            patternlist = [pattern1, pattern2]
    
                            for pattern in patternlist:
    
                                match = re.search(pattern, newline)
    
                                if match:
    
                                    numbermatch = re.search(pattern3, newline)
    
                                    if numbermatch:
    
                                        start, finish = numbermatch.span()
    
                                        before = newline[:start].strip()
                                        after = newline[start:].strip()
                                        befores.append(before)
                                        afters.append(after)
                                        
                                        
                                      
                                       
                                 
                                       
                                           
                                    try:
                                            matches = list(re.finditer(pattern3, after))
                                            mumpsmatch = mumps_index[yearposition]
                                          
                                            mumps = matches[mumpsmatch].group()
                
                                            mumpsgroup.append(mumps)
                                            
                                    except IndexError as e:
                                        f"Error, index out of range {e}"
                                        
                                        try:
                                            mumpsmatch = mumps_index[yearposition]
                                            mumps = matches[mumpsmatch].group()
                                            if mumpsmatch==8:
                                                mumpsgroup.append(mumps)
                                                
                                            elif mumpsmatch<8:
                                             
                                                mumpsgroup.append("error, please check!")
                                           
                                            
                                        except IndexError:
                                            
                                            print("error")
                                            
                                            
                                           
        
        
                                        break
    
    
    
                for i, item in enumerate(afters):
                    print(f"Index {i}: {item}")
                afterdf=pd.DataFrame()
                afterdf['mumps_firstrun']=afters
                afterdf['YEAR']=year
                cols=list(afterdf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                afterdf=afterdf[cols]
                afterdf.to_csv(filedirectory / rf"csv\after\mumps\{year}.csv",index=False).mkdir(parents=True, exist_ok=True)
    
                for i, item in enumerate(befores):
                    print(f"Index {i}: {item}")
                beforedf=pd.DataFrame()
                beforedf['states']=befores
                beforedf['YEAR']=year
                cols=list(beforedf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                beforedf=beforedf[cols]
                beforedf.to_csv(filedirectory / rf"csv\before\mumps\{year}.csv",index=False).mkdir(parents=True, exist_ok=True)
                for i, item in enumerate(mumpsgroup):
                    print(f"Mumps {i}: {item}")
                mumpssdf=pd.DataFrame()
                mumpssdf['mumps']=mumpsgroup
                
                mumpssdf['YEAR']=year
                cols=list(mumpssdf.columns)
                cols[0],cols[1]=cols[1],cols[0]
                mumpssdf=mumpssdf[cols]
                mumpssdf.to_csv(filedirectory / rf"csv\mumps\{year}.csv",index=False).mkdir(parents=True, exist_ok=True)   
                
    
    group=['after','before','mumps']
    
    
    
    
    
    for member in group:
        dataframecsvfiles=Path(savepath / fr"\csv\{member}\mumps").mkdir(parents=True, exist_ok=True)
        if member=='mumps':
          dataframecsvfiles=Path(savepath / fr"\csv\{member}").mkdir(parents=True, exist_ok=True)  
        csv_list = list(dataframecsvfiles.glob("*.csv"))
        combineddf=pd.concat((pd.read_csv(file) for file in csv_list),ignore_index=True)
        combineddf.to_csv(dataframecsvfiles / r"combined.csv",index=False)     
    
    

