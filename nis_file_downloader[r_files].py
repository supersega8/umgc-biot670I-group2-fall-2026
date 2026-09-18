# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 18:57:22 2026

@author: sumit
"""

import pandas as pd
import urllib.request
from urllib.error import HTTPError
from pathlib import Path

editions = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
years = [2015, 2016, 2017, 2018, 2019,
         2020, 2021, 2022, 2023, 2024]

downloadpath = Path(
    input("Enter the folder where you want to save the CDC files: ")
)

downloadpath.mkdir(parents=True, exist_ok=True)


for edition, year in zip(editions, years):

    # CDC changed the location of the newer files
    if edition ==15:
        url = (
            "https://www.cdc.gov/vaccines/imz-managers/nis/downloads/nis-puf15.r"
        )

    else:
        url = (
            f"https://ftp.cdc.gov/pub/Vaccines_NIS/NISPUF{edition}.R"
        )

   

    filename = downloadpath / f"NISPUF{edition}.R"

    try:
        urllib.request.urlretrieve(url, filename)

        print(
            f"{year} successfully saved to: {filename}"
        )

    except HTTPError as e:
        print(
            f"Could not download {year}: "
            f"HTTP {e.code}"
        )
        