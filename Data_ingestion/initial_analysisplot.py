# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 01:58:03 2026

@author: sumit
"""

import pandas as pd
import numpy as np
from pathlib import Path
from plotnine import ggplot, aes, labs,geom_point, geom_smooth, theme_minimal
from plotnine.data import mtcars

filepath=Path(input(r"put the analysis.csv in this folder"))

df=pd.read_csv(filepath / r"analysis.csv")

source_data=df[['YEAR','weighted_rate']]
#using the local regression to get a curved fit, since data may be non-linear
plot=(
      ggplot(source_data,aes(x='YEAR',y='weighted_rate'))+
      geom_point(size=3) +
      labs(title="Vaccination rates from 1995-2024 for MMR")+
      geom_smooth(method='lowess',span=0.5,se=True,color='blue') +
      theme_minimal())

plot.save(filepath / r"plot.png")