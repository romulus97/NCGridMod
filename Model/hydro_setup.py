# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 00:55:57 2020

@author: jkern
"""

import pandas as pd
import numpy as np

# get catawba data
df_catawba = pd.read_csv('cheops.csv')
catawba_dams = list(df_catawba.columns)
catawba_cap = 0
for i in catawba_dams:
    catawba_cap += max(df_catawba[i])/24

df = pd.read_excel('Hydro_location.xlsx',sheet_name='all')
substations = list(df['Substation'].unique())

names = []
caps = []

for s in substations:
    
    sample = df[df['Substation'] == s]
    
    a = sample.iloc[0,5]
    a = a.replace(" ","")
    a = a.replace("(","")
    a = a.replace(")","")
    names.append(a)
    caps.append(sum(sample['capacity']))
    
df_hydro_gens = pd.DataFrame()
df_hydro_gens['name'] = names
df_hydro_gens['node'] = substations
df_hydro_gens['cap'] = caps
df_hydro_gens.to_csv('gens_hydro.csv')

mwh = np.zeros((365,len(names)))

for d in names:
    idx = names.index(d)
    if d in catawba_dams:
        for i in range(0,365):
            mwh[i,idx] = df_catawba.loc[i,d]
    else:
        ratio = caps[idx]/catawba_cap
        for i in range(0,365):
            mwh[i,idx] = sum(df_catawba.loc[i,:])*ratio
        
df_out = pd.DataFrame()
for d in names:
    idx = names.index(d)
    df_out[d] = mwh[:,idx]
    
df_out.to_csv('data_hydro.csv')
