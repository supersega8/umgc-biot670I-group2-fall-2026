# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:35:01 2026

@author: sumit
"""


from pathlib import Path
import pandas as pd


filepath=Path(input(r"Tell me the path where the raw csv files are: "))
files = sorted(filepath.glob("*.csv"))

cleanedcsvfilepath=Path(input(r"Tell me the path where the cleaned up csv files should go: "))

#index string splitting data from 1995-2024

indexstring = "95,96,97,98,99,00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24"
index=indexstring.split(",")
#provider weight varies slightly between years/datasets. This dictionary normalises them
provider_weight_dictionary_lookup={
    '95':'HY_WGT',
    '96':'HY_WGT',    
    '97':'HY_WGT',
    '98':'HY_WGT',
    '99':'HY_WGT',
    '00':'HY_WGT',
    
    '01':'HY_WGT',

    '02':'WT',
    '03':'WGT',
    '04':'WGT',
    
    '05':'PROVWT',
    
    '06':'PROVWT',
'07':'PROVWT',
'08':'PROVWT',
'09':'PROVWT',
'10':'PROVWT',
'11':'PROVWT_LL',
'12':'PROVWT_D',
'13':'PROVWT_D',
'14':'PROVWT_D',
'15':'PROVWT_D',
'16':'PROVWT_D',
'17':'PROVWT_D',
'18':'PROVWT_C',
'19':'PROVWT_C',
'20':'PROVWT_C',
'21':'PROVWT_C',
'22':'PROVWT_C',
'23':'PROVWT_C',
'24':'PROVWT_C',
}

#looping through every file for the cleanup

print("CSV files found:", len(files))
print("Indexes:", len(index))

for file in files:
    print(file.name)
#index stem to test the years eg 95.csv 96.csv, etc. 
    idx = file.stem[-2:]

    if idx not in provider_weight_dictionary_lookup:
        print(f"No provider weight defined for {idx}. Skipping {file.name}")
        continue

    provider_weight = provider_weight_dictionary_lookup[idx]
#pandas dataframe columns
    columns = [
        'SEQNUMC',
        'YEAR',
        'STATE',
        provider_weight,
        'P_NUMMMX',
        'P_NUMMP',
        'P_NUMMPR',
        'P_NUMMRV',
        'P_NUMMS',
        'P_NUMMSM',
        'P_NUMMSR',
        'P_NUMOLN',
        'P_NUMPOL',
        'P_NUMRB'
    ]
    
    fips_state = {
    1: "Alabama",
    2: "Alaska",
    4: "Arizona",
    5: "Arkansas",
    6: "California",
    8: "Colorado",
    9: "Connecticut",
    10: "Delaware",
    11: "District of Columbia",
    12: "Florida",
    13: "Georgia",
    15: "Hawaii",
    16: "Idaho",
    17: "Illinois",
    18: "Indiana",
    19: "Iowa",
    20: "Kansas",
    21: "Kentucky",
    22: "Louisiana",
    23: "Maine",
    24: "Maryland",
    25: "Massachusetts",
    26: "Michigan",
    27: "Minnesota",
    28: "Mississippi",
    29: "Missouri",
    30: "Montana",
    31: "Nebraska",
    32: "Nevada",
    33: "New Hampshire",
    34: "New Jersey",
    35: "New Mexico",
    36: "New York",
    37: "North Carolina",
    38: "North Dakota",
    39: "Ohio",
    40: "Oklahoma",
    41: "Oregon",
    42: "Pennsylvania",
    44: "Rhode Island",
    45: "South Carolina",
    46: "South Dakota",
    47: "Tennessee",
    48: "Texas",
    49: "Utah",
    50: "Vermont",
    51: "Virginia",
    53: "Washington",
    54: "West Virginia",
    55: "Wisconsin",
    56: "Wyoming"
}

    print(f"Processing {file.name} -> {idx}")
    
    

    try:
       df = pd.read_csv(file, low_memory=False)
       
       

       available_columns = []
       
       for column in columns:
            if column not in df.columns:
                print(f"{column} not found in {file.name}")
                continue

            available_columns.append(column)
        #always makea copy of the df and keep it in a new df object/variable
       cleaned_df = df[available_columns].copy()
       
    # Standardize provider weight
       cleaned_df.rename(
            columns={provider_weight: 'PROVWT'},
            inplace=True
        )
       
       
    
        # Rename state code
       cleaned_df.rename(
            columns={'STATE': 'FIPS_CODE'},
            inplace=True
        )
    
       
       cleaned_df.insert(3,'state_name',cleaned_df['FIPS_CODE'].map(fips_state),allow_duplicates=False)
       
 #getting the weighted/unweighted vaccination rates 
       cleaned2 = cleaned_df[
    cleaned_df['PROVWT'].notna() &
    cleaned_df['P_NUMMMX'].notna()
].copy()

       cleaned2["MMR_1PLUS"] = (cleaned2['P_NUMMMX'] >= 1).astype(int)

       cleaned2['unweighted_rate'] = cleaned2["MMR_1PLUS"].mean() * 100

       
       
       cleaned2['weighted_rate']= (
    (cleaned2["MMR_1PLUS"] * cleaned2["PROVWT"]).sum()
    / cleaned2["PROVWT"].sum()
) * 100

       
       
       

    
       cleaned_df.to_csv(
            cleanedcsvfilepath / f"first_cleaned{idx}.csv",
            index=False
        )
       cleaned2.to_csv(
            cleanedcsvfilepath / rf"second_cleaned\second_cleaned{idx}.csv",
            index=False
        )
       
       
       
      
      
     
      
      
       
  
    
       

    except Exception as e:
        print(f"Failed {idx}: {e}")
        
    try:
        secondfilepath=Path(cleanedcsvfilepath /"second_cleaned" )
        secondfilepath.mkdir(parents=True,exist_ok=True)
        cleanedfiles = sorted(secondfilepath.glob("*.csv"))
        
        analysis=pd.DataFrame()
        for cleanfile in cleanedfiles:
            cleaned3 = pd.read_csv(
        cleanfile,
        low_memory=False
    )
#creating another DF with the years and weighted vaccination rates to do a plot comparison later 
            firstrow = cleaned3[
        ['YEAR', 'weighted_rate']
    ].head(1)

            analysis = pd.concat(
        [analysis, firstrow],
        ignore_index=True
    )
        final_analysis=analysis.drop_duplicates(subset=['YEAR']).sort_values(by=['YEAR'])
        
        final_analysis.to_csv(secondfilepath / "analysis.csv",index=False)
    
    except Exception as e2:
        print(f"Failed: {e2}")        
