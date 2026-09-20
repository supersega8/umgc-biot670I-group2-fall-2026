# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 22:16:43 2026

@author: sumit
"""
from pathlib import Path
import urllib.request
from urllib.error import HTTPError, URLError

#this index can be changed , basically corresponds to the years of data to be downloaded 
original_index = [
    
     '06', '07', '08', '09',
    '10', '11', '12', '13', '14',
     '16', '17', '18', '19',
    '20', '21', '22', '23', '24'
]

url_file_ask = Path(input(r"please put the 'r_hyperlinks.txt' file in this directory, please specify the directory: "))

url_file=(url_file_ask/r"r_hyperlinks.txt")

download_path = Path(input(r"Tell me where you want to store these files: "))

filecontent = url_file.read_text().splitlines()
#cleaning the r_hyperlinks.txt file
cleaned_list = [
    item.strip()
    for item in filecontent
    if item.strip()
]
#for loop that loops through each of the indexes against they hyperlink, if no URL found for that index, it states it as so
for number in original_index:

    matching_url = None

    for item in cleaned_list:

        if number in item:
            matching_url = item
            break

    if matching_url is None:
        print(f"No URL found for {number}")
        continue
    
    #using pathlib module and a try-except block to batch download the files 
   
    downloadedfile = (
                download_path /
                f"NISPUF{number}.R"
            )
    try:
                urllib.request.urlretrieve(
                    matching_url,
                    downloadedfile)
            
                print(f"Downloading {number}...")
                print(matching_url)
                print(
                    f"Successfully downloaded NIS year R file {number}"
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
        
