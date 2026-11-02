# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:52:32 2026

@author: sumit
"""

import requests

from bs4 import BeautifulSoup

import re

import pandas as pd

from pathlib import Path

url_list = [
    "https://www.cdc.gov/mmwr/preview/mmwrhtml/00044418.htm",
    "https://www.cdc.gov/mmwr/preview/mmwrhtml/00050719.htm",
    "https://www.cdc.gov/MMWR/Preview/MMWRhtml/00056071.htm",
    "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm4753a1.htm",
    "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm4853a1.htm",
    "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm4953a1.htm",
    "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm5053a1.htm",
    "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm5153a1.htm"
]

year_list = [
    '1995', '1996', '1997', '1998',
    '1999', '2000', '2001', '2002'
]

diseases = ['measles', 'mumps', 'rubella']

# Folder locations
filepathuser = Path(input(
    "Where should the MMWR text files be saved? "
).strip().strip('"'))

savepathinput = Path(input(
    "Where should the CSV files be saved? "
).strip().strip('"'))

filepathuser.mkdir(parents=True, exist_ok=True)
savepathinput.mkdir(parents=True, exist_ok=True)

folders = [
    'csv', 'before', 'after',
    'measles', 'mumps', 'rubella',
    '1995-1997 data'
]

for folder in folders:
    (savepathinput / folder).mkdir(parents=True, exist_ok=True)


# Disease columns in the original MMWR tables.
# Positions are relative to the first numeric column.
column_positions = {
    '1995-1997': {
        'measles': [0, 1],
        'mumps': [3],
        'rubella': [4]
    },
    '1998': {
        'measles': [1, 2],
        'mumps': [4],
        'rubella': [1]
    }
}


# Download the reports once, rather than once per disease.
for year, url in zip(year_list, url_list):

    print(f"\nProcessing year: {year}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Could not retrieve {year}: {error}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    filepath = filepathuser / f"{year}.txt"

    with filepath.open(mode='w', encoding='utf-8') as file:
        file.write(soup.get_text("\n"))

    # The 1999-2002 summary HTML pages do not contain
    # the same directly extractable state tables.
    if int(year) >= 1999:
        print(f"{year}: saved text; table extraction skipped.")
        continue

    if int(year) <= 1997:
        positions = column_positions['1995-1997']
    else:
        positions = column_positions['1998']

    # Process each disease separately.
    for disease in diseases:

        befores = []
        afters = []
        diseasegroup = []

        # Preformatted tables are used in earlier reports.
        blocks = soup.find_all('pre')

        if not blocks:
            blocks = soup.find_all('table')

        for table in blocks:

            data = table.get_text()

            if disease not in data.lower():
                continue

            if "area" not in data.lower():
                continue

            # Read either HTML table cells or preformatted lines.
            if table.name == 'table' and table.find('tr'):

                rows = []

                for tr in table.find_all('tr'):
                    cells = [
                        cell.get_text(" ", strip=True)
                        for cell in tr.find_all(
                            ['td', 'th'], recursive=False
                        )
                    ]

                    if cells:
                        rows.append(cells)

            else:
                rows = [
                    re.split(r"\s{2,}", line.strip())
                    for line in data.splitlines()
                ]

            area_flag = False
            selected_positions = positions[disease]

            for parts in rows:

                if not parts:
                    continue

                state = parts[0].strip()

                # Start after the table header.
                if state.lower() == 'area':
                    area_flag = True
                    continue

                if not area_flag:
                    continue

                # Stop before territorial data.
                if state.lower().startswith('guam'):
                    break

                values = parts[1:]

                if len(values) <= max(selected_positions):
                    continue

                # Replace only missing-case markers with zero.
                # Preserve NA and NN as unavailable/not notifiable.
                values = [
                    '0' if value in ['-', '--', '---']
                    else value
                    for value in values
                ]

                # Make sure the selected cells are valid counts.
                selected = [
                    values[index]
                    for index in selected_positions
                ]

                if not all(
                    re.fullmatch(r"\d[\d,]*|NA|NN", value, re.I)
                    for value in selected
                ):
                    continue

                # Retain the state and full row for inspection.
                befores.append(state)
                afters.append(" ".join(values))

                if disease == 'measles':
                    diseasegroup.append(
                        f"{selected[0]},{selected[1]}"
                    )
                else:
                    diseasegroup.append(selected[0])

            # Stop after locating the appropriate table.
            if diseasegroup:
                break

        if not diseasegroup:
            print(f"No data found: {year} - {disease}")
            continue

        # -----------------------------------
        # After DataFrame
        # -----------------------------------
        afterdf = pd.DataFrame()

        afterdf[f'{disease}_firstrun'] = afters
        afterdf['YEAR'] = year

        cols = list(afterdf.columns)
        cols[0], cols[1] = cols[1], cols[0]
        afterdf = afterdf[cols]

        afterdf.to_csv(
            savepathinput / 'after' / f"{year}_{disease}.csv",
            index=False
        )

        # -----------------------------------
        # Before DataFrame
        # -----------------------------------
        beforedf = pd.DataFrame()

        beforedf['states'] = befores
        beforedf['YEAR'] = year

        cols = list(beforedf.columns)
        cols[0], cols[1] = cols[1], cols[0]
        beforedf = beforedf[cols]

        beforedf.to_csv(
            savepathinput / 'before' / f"{year}_{disease}.csv",
            index=False
        )

        # -----------------------------------
        # Disease DataFrame
        # -----------------------------------
        diseasedf = pd.DataFrame()

        diseasedf[disease] = diseasegroup
        diseasedf[disease] = diseasedf[disease].astype("string")

        if disease == 'measles':

            diseasedf[['indigenous', 'imported']] = (
                diseasedf['measles'].str.split(
                    ',', n=1, expand=True
                )
            )

            diseasedf['YEAR'] = year

            cols = list(diseasedf.columns)
            cols[0], cols[3] = cols[3], cols[0]
            diseasedf = diseasedf[cols]

        else:

            diseasedf['YEAR'] = year

            cols = list(diseasedf.columns)
            cols[0], cols[1] = cols[1], cols[0]
            diseasedf = diseasedf[cols]

        diseasedf.to_csv(
            savepathinput / disease / f"{year}.csv",
            index=False
        )

        print(
            f"Saved {len(diseasedf)} rows "
            f"for {disease}, {year}"
        )


# -----------------------------------
# Combine yearly CSV files
# -----------------------------------
for disease in diseases:

    group = ['after', 'before', disease]

    for member in group:

        dataframecsvfiles = savepathinput / member

        csv_list = sorted(
            file for file in dataframecsvfiles.glob("*.csv")
            if file.name != "combined.csv"
        )

        if not csv_list:
            print(f"No CSV files found in {member}")
            continue

        combineddf = pd.concat(
            (pd.read_csv(file) for file in csv_list),
            ignore_index=True
        )

        combinedfolder = (
            savepathinput / '1995-1997 data' / member
        )

        combinedfolder.mkdir(
            parents=True,
            exist_ok=True
        )

        combineddf.to_csv(
            combinedfolder / "combined.csv",
            index=False
        )

        print(f"Combined CSV saved: {member}")

print("\nFinished processing available MMWR tables.")

                