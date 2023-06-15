# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:35:13 2020

@author: jkern
"""

import pandas as pd
import numpy as np

df_gen = pd.read_csv('data_genparams.csv',header=0)
gen_nodes = list(df_gen['node'].unique())

df = pd.read_csv('data_transparams.csv',header=0)
sources = df.loc[:,'source']
sinks = df.loc[:,'sink']
combined = np.append(sources, sinks)
df_combined = pd.DataFrame(combined,columns=['node'])
trans_nodes = list(df_combined['node'].unique())

combined = np.append(gen_nodes,trans_nodes)
df_combined = pd.DataFrame(combined,columns=['node'])
all_nodes = list(df_combined['node'].unique())

#node lists
df_nodes_G = pd.read_excel('node_lists.xlsx',sheet_name = 'generation_only')
df_nodes_D = pd.read_excel('node_lists.xlsx',sheet_name = 'demand_only')
df_nodes_N = pd.read_excel('node_lists.xlsx',sheet_name = 'neither')

G = list(df_nodes_G['Name'])
D = list(df_nodes_D['Name'])
N = list(df_nodes_N['Name'])

missing= []

for i in all_nodes:
    if i in G or i in D or i in N:
        pass
    else:
        missing.append(i)

df_missing = pd.DataFrame(missing)
df_missing.to_csv('missing.csv')
        
