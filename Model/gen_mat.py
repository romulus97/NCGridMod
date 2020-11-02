# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 00:47:29 2020

@author: jkern
"""

import pandas as pd
import numpy as np

df = pd.read_csv('data_genparams_partial.csv',header=0)
for i in range(0,len(df)):
    df.loc[i,'node'] = 'n_' + str(df.loc[i,'node'])
    
gens = df.loc[:,'name']

all_nodes = pd.read_csv('unique_nodes.csv', header=0,index_col=0)##Generation nodes without demand
all_nodes.columns = ['Name']
all_nodes = list(all_nodes['Name'])  

A = np.zeros((len(gens),len(all_nodes)))

df_A = pd.DataFrame(A)
df_A.columns = all_nodes

for i in range(0,len(gens)):
    node = df.loc[i,'node']
    df_A.loc[i,node] = 1

df_A.to_csv('gen_mat.csv')

