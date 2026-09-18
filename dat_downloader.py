# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 22:16:43 2026

@author: sumit
"""
from pathlib import Path
import urllib.request
from urllib.error import HTTPError, URLError
import zipfile

original_index = [
    '95', '96', '97', '98', '99',
    '00', '01', '02', '03', '04',
    '05', '06', '07', '08', '09',
    '10', '11', '12', '13', '14',
    '15', '16', '17', '18', '19',
    '20', '21', '22', '23', '24'
]

url_file_ask = Path(input(r"please put the 'cdc_hyperlinks.txt' file in this directory, please specify the directory: "))

url_file=(url_file_ask/r"cdc_hyperlinks.txt")

download_path = Path(input(r"Tell me where you want to store these files: "))

filecontent = url_file.read_text().splitlines()

cleaned_list = [
    item.strip()
    for item in filecontent
    if item.strip()
]

for number in original_index:

    matching_url = None

    for item in cleaned_list:

        if number in item:
            matching_url = item
            break

    if matching_url is None:
        print(f"No URL found for {number}")
        continue
    
    
    if matching_url.lower().endswith(".zip"):
            downloadedfile=(download_path / f"NISPUF{number}.DAT.zip")
            try:
                urllib.request.urlretrieve(matching_url,downloadedfile)
                if zipfile.is_zipfile(downloadedfile):
                    with zipfile.ZipFile(downloadedfile,"r") as zip_ref:
                        zip_ref.extractall(download_path)
                        print(f"Downloaded and extracted NISPUF{number}")
                    downloadedfile.unlink()
                        
            except HTTPError as e: 

                print(
                    f"Could not download {number}: "
                    f"HTTP {e.code}"
                )

            except URLError as e:

                print(
                    f"Could not download {number}: "
                    f"{e.reason}"
                )
    else:
            downloadedfile = (
                download_path /
                f"NISPUF{number}.DAT"
            )
            try:
                urllib.request.urlretrieve(
                    matching_url,
                    downloadedfile)
            
                print(f"Downloading {number}...")
                print(matching_url)
                print(
                    f"Successfully downloaded NIS year {number}"
                )

    

            except HTTPError as e:
        
                print(
                    f"Could not download {number}: "
                    f"HTTP {e.code}"
                )
        
            except URLError as e:
        
                print(
                    f"Could not download {number}: "
                    f"{e.reason}"
                )
        
