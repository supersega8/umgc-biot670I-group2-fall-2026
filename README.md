# umgc-biot670I-group2-fall-2026

UMGC Biotechnology capstone group 2 Fall 2026 Repository 

This GitHub includes all relevant source code for this project. The project is essentially an ETL pipeline with data analysis. The visual dashboard is done on Power BI. 

The project is essentially broken down into 6 sections:

1) tycho_data_analysis- The historical decline of measles cases after introduction of the 1963 vaccine. This serves as the positive control for our project. Primarily coded in R for graphical visualization with Pandas for creation of a cleaned table. 

2) Source_data_download- used to download the vaccination source data. Sources for this data include, but not limited to:

NIS child datasets (aged 19-35 months):

https://www.cdc.gov/nis/php/datasets-child/index.html
https://www.cdc.gov/nchs/nis/data_files.htm
https://www.cdc.gov/nchs/nis/data_files_09_prior.htm

Also includes the download of the necessary R/SAS files to properly extract the data from the .DAT files 

3) vaccination_data_ingestion- Pipeline to take vaccination data from 1995-2024 .RData files to create cleaned .CSV files grouped by year, state, and a STATE_WEIGHTED vaccination rate (where child received at least one MMR dose).

4) disease_incidence_ingestion- used to download and clean the disease-incidence data from 1995-2024. Since Project Tycho had inconsistent state-level data, the National Notifiable Diseases Surveillance System (NNDSS) tables were used. Many tables (prior to 2016) were only available in pdf/html format, so separate scripts were used to extract the relevant tables from each year.

https://www.cdc.gov/ncird-surveillance/about/nndss.html

5) Harmonization- used to merge the Vaccination rate and disease_incidence datasets

6) Analysis- Spearman and Pearson correlations with 1-to-3-year time-lag associations. Heatmaps and scatterplot images generated after analysis

Please see requirements.txt for relevant libraries needed for this 
