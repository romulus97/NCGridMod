# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 22:49:16 2020

@author: jkern
"""

import pandas as pd

df_data = pd.read_csv('data_solar.csv',header=0)

nodes = list(df_data.columns)

new_nodes = []

for n in nodes:
    new = 'n_' + str(n) + '_solar'
    new_nodes.append(new)


    