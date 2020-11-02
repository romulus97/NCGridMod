# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 00:47:29 2020

@author: jkern
"""

import pandas as pd
import numpy as np

df = pd.read_csv('data_transparams.csv',header=0)

L = []
lines= []
reactance = []
limit = []
sources = []
sinks = []
        
for i in range(0,len(df)):
    s = df.loc[i,'source']
    k = df.loc[i,'sink']
    s = 'n_' + str(s)
    k = 'n_' + str(k)
    line = s + '_' + k
           
    if line in lines:
        
        idx = lines.index(line)
        reactance[idx] = max(1/df.loc[i,'linesus'],reactance[idx])
        limit[idx] = limit[idx] + df.loc[i,'linemva']
       
    else:
        
        lines.append(line)
        
        reactance.append(1/df.loc[i,'linesus'])
        limit.append(df.loc[i,'linemva'])
        sources.append(s)
        sinks.append(k)

df_line_params = pd.DataFrame()
df_line_params['source'] = sources
df_line_params['sink'] = sinks
df_line_params['reactance'] = reactance
df_line_params['limit'] = limit 
df_line_params.to_csv('unique_trans.csv')


