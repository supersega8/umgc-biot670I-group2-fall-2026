# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:20:26 2026

@author: sumit
"""

import seaborn as sns
import pandas as pd
from scipy.stats import spearmanr,pearsonr
from pathlib import Path
import matplotlib.pyplot as plt

#this will create heatmaps and scatterplots, since the heatmaps are better able to display the variable
#spearman/pearson coefficents since they do not follow an overall trend

filepath=Path(input(r"""Tell me the filepath to where the time-lagged state level disease data is. 
                    The data should include 3 analysis csv's for each disease ending in 
                    state_analysis.csv. do not include the actual csv yet:  """))

savepath=Path(input("tell me where you would like to save the processed images after analyis?: "))

diseases = ['MEASLES', 'MUMPS', 'RUBELLA']
years={'one','two','three'}

for disease in diseases:
    for item in years:
        df=pd.read_csv(filepath / fr"{disease}_{item}_yearlag_state_analysis.csv")
        heatmapdf = df.set_index('FIPS_CODE')[
            ['spearman-correlation', 'pearson-correlation']
        ]
    
        plt.figure(figsize=(8, 14))
    
        sns.heatmap(
            heatmapdf,
            annot=True,
            cmap='coolwarm',
            center=0,
            vmin=-1,
            vmax=1,
            fmt='.2f',
            linewidths=0.3,
            cbar_kws={'label': 'Correlation Coefficient'}
        )
    
        plt.title(f'State-Level Time-Lagged Correlations,{disease},{item} year')
        plt.xlabel('Correlation Method')
        plt.ylabel('State FIPS Code')
        plt.tight_layout()
        
        plt.savefig(savepath / fr"{disease}_{item}yearlag_heatmap.png")
        
       
        
        
        ax=df.plot.scatter(x='FIPS_CODE',y='pearson-correlation',color='blue',label='pearson-stat',
                        figsize=(20,5),
                        title=f'{disease} stats, time-lag {item}')
       
        bx=df.plot.scatter(x='FIPS_CODE',y='spearman-correlation',color='red',label='spearman-stat',ax=ax,
                        figsize=(20,5),
                        title=f'{disease} stats, time-lag {item}')
        
        df.apply(lambda row: ax.text(row["FIPS_CODE"] + 0.05, row['pearson-correlation'], row["FIPS_CODE"]), axis=1)
        df.apply(lambda row: bx.text(row["FIPS_CODE"] + 0.05, row['spearman-correlation'], row["FIPS_CODE"]), axis=1)
        plt.ylabel("coefficient value")
        plt.show()
        