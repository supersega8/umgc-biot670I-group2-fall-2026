# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 18:57:22 2026

@author: sumit
"""
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
    if edition <= 22:
        url = (
            f"https://ftp.cdc.gov/pub/Vaccines_NIS/"
            f"NISPUF{edition}.DAT"
        )

    elif edition == 23:
        url = (
            "https://www.cdc.gov/nis/media/files/2024/11/"
            "NISPUF23.DAT"
        )

    elif edition == 24:
        url = (
            "https://www.cdc.gov/nis/media/files/2026/05/"
            "NISPUF24.DAT"
        )

    filename = downloadpath / f"NISPUF{edition}.DAT"

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
        