# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:35:01 2026

@author: sumit
"""


from pathlib import Path
import pandas as pd
import numpy as np

filepath=Path(r"C:\Users\sumit\Documents\CDC NIS data 2015-2024\csv")
files = sorted(filepath.glob("*.csv"))

cleanedcsvfilepath=Path(r"C:\Users\sumit\Documents\CDC NIS data 2015-2024\csv\cleaned_csv_1stround")



indexstring = "06,07,08,09,10,11,12,13,14,16,17,18,19,20,21,22,23,24"
index=indexstring.split(",")

provider_weight_dictionary_lookup={'06':'PROVWT',
'07':'PROVWT',
'08':'PROVWT',
'09':'PROVWT',
'10':'PROVWT',
'11':'PROVWT_LL',
'12':'PROVWT_D',
'13':'PROVWT_D',
'14':'PROVWT_D',
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



print("CSV files found:", len(files))
print("Indexes:", len(index))

for file in files:
    print(file.name)

for file, idx in zip(files, index):

    provider_weight = provider_weight_dictionary_lookup[idx]

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
    
    statename_result=list(map(fips_state.get,columns[2]))

    try:
       df = pd.read_csv(file,low_memory=False)
       
  

       cleaned_df = df[columns].copy()
      

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
    
       """ # Map FIPS code directly to state name
       cleaned_df['state_name'] = (
            cleaned_df['FIPS_CODE'].map(fips_state)
        )"""
       
       cleaned_df.insert(3,'state_name',cleaned_df['FIPS_CODE'].map(fips_state),allow_duplicates=False)
       
 
       

    
       cleaned_df.to_csv(
            cleanedcsvfilepath / f"first_cleaned{idx}.csv",
            index=False
        )

       print(f"Finished {idx}")
       
       
       valid = cleaned_df[
    cleaned_df['PROVWT'].notna() &
    cleaned_df['P_NUMMMX'].notna()
].copy()

       valid["MMR_1PLUS"] = (valid['P_NUMMMX'] >= 1).astype(int)

       unweighted_rate = valid["MMR_1PLUS"].mean() * 100

       print(unweighted_rate)
       
       weighted_rate = (
    (valid["MMR_1PLUS"] * valid["PROVWT"]).sum()
    / valid["PROVWT"].sum()
) * 100

       print(weighted_rate)
    


    except Exception as e:
        print(f"Failed {idx}: {e}")
        
        
