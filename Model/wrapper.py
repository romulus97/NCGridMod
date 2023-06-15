# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from MTS_MILP import model as m1
from MTS_LP import model as m2
from pyomo.core import Var
from pyomo.core import Constraint
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime
import pyomo.environ as pyo
from pyomo.environ import value

#Outputs folder
#folder = '/home/lprieto/Research/M2S_line_outages/Outputs/'
folder_2 = '/home/lprieto/Research/M2S_line_outages/Outputs_2/'

# Max = 365
days = 365

instance = m1.create_instance('MTS_data.dat')
instance2 = m2.create_instance('MTS_data.dat')
instance2.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

opt = SolverFactory("gurobi")
opt.options["threads"] = 8

H = instance.HorizonHours
D = 2
K=range(1,H+1)


#Space to store results
mwh=[]
on=[]
switch=[]
flow=[]
# srsv=[]
# nrsv=[]
slack = []
vlt_angle=[]
duals=[]

df_generators = pd.read_csv('data_genparams_partial.csv',header=0)


#max here can be (1,365)
for day in range(1,days):
    
    for z in instance.buses:
    #load Demand and Reserve time series data
        for i in K:
            instance.HorizonDemand[z,i] = instance.SimDemand[z,(day-1)*24+i]
            instance2.HorizonDemand[z,i] = instance.SimDemand[z,(day-1)*24+i]

            # instance.HorizonReserves[i] = instance.SimReserves[(day-1)*24+i]

    for z in instance.lines:
        for i in K:
            instance.HorizonLineLimit[z,i] = instance.SimLineLimit[z,(day-1)*24+i]
            instance2.HorizonLineLimit[z,i] = instance2.SimLineLimit[z,(day-1)*24+i]

    for z in instance.Hydro:
    #load Hydropower time series data
        for i in K:
            instance.HorizonHydro[z,i] = instance.SimHydro[z,(day-1)*24+i]
            instance2.HorizonHydro[z,i] = instance.SimHydro[z,(day-1)*24+i]
        
    for z in instance.Solar:
    #load Solar time series data
        for i in K:
            instance.HorizonSolar[z,i] = instance.SimSolar[z,(day-1)*24+i]
            instance2.HorizonSolar[z,i] = instance.SimSolar[z,(day-1)*24+i]

    for z in instance.Nuc:
    #load Nuclear time series data
        for i in K:
            instance.HorizonNuc[z,i] = instance.SimNuc[z,(day-1)*24+i]
            instance2.HorizonNuc[z,i] = instance.SimNuc[z,(day-1)*24+i]

    result = opt.solve(instance,tee=True,symbolic_solver_labels=True) ##,tee=True to check number of variables\n",
    instance.solutions.load_from(result)  
    
    print('MILP done')
    
    for j in instance.Dispatchable:
        for t in K:
            if value(instance.on[j,t]) == 1:
                instance2.on[j,t] = 1
                instance2.on[j,t].fixed = True
            else:
                instance.on[j,t] = 0
                instance2.on[j,t] = 0
                instance2.on[j,t].fixed = True

            if value(instance.switch[j,t]) == 1:
                instance2.switch[j,t] = 1
                instance2.switch[j,t].fixed = True
            else:
                instance2.switch[j,t] = 0
                instance2.switch[j,t] = 0
                instance2.switch[j,t].fixed = True
                    
    results = opt.solve(instance2,tee=True,symbolic_solver_labels=True)
    instance2.solutions.load_from(results)
    
    print('LP done')

    for c in instance2.component_objects(Constraint, active=True):
        cobject = getattr(instance2, str(c))
        if str(c) in ['Node_Constraint']:
            for index in cobject:
                 if int(index[1]>0 and index[1]<25):
                     try:
                         duals.append((str(c),index[0],index[1]+((day-1)*24), instance2.dual[cobject[index]]))
                     except KeyError:
                         duals.append((str(c),index[0],index[1]+((day-1)*24),-999))

    for v in instance.component_objects(Var, active=True):
        varobject = getattr(instance, str(v))
        a=str(v)
                  
        # if a=='Theta':
        #     for index in varobject:
        #         if int(index[1]>0 and index[1]<25):
        #             if index[0] in instance.buses:
        #                 vlt_angle.append((index[0],index[1]+((day-1)*24),varobject[index].value))
                        
        if a=='mwh':
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    mwh.append((index[0],index[1]+((day-1)*24),varobject[index].value))                                            
        
        # if a=='on':  
        #     for index in varobject:
        #         if int(index[1]>0 and index[1]<25):
        #             on.append((index[0],index[1]+((day-1)*24),varobject[index].value))

        # if a=='switch':
        #     for index in varobject:
        #         if int(index[1]>0 and index[1]<25):
        #             switch.append((index[0],index[1]+((day-1)*24),varobject[index].value))
                    
        if a=='S':    
            for index in varobject:
                if index[0] in instance.buses:
                        slack.append((index[0],index[1]+((day-1)*24),varobject[index].value))

        if a=='Flow':    
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    flow.append((index[0],index[1]+((day-1)*24),varobject[index].value))                                            

        # if a=='srsv':    
        #     for index in varobject:
        #         if int(index[1]>0 and index[1]<25):
        #             srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value))

        # if a=='nrsv':    
        #     for index in varobject:
        #         if int(index[1]>0 and index[1]<25):
        #             nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value))

    print(day)
        
# vlt_angle_pd=pd.DataFrame(vlt_angle,columns=('Node','Time','Value'))
mwh_pd=pd.DataFrame(mwh,columns=('Generator','Time','Value'))
# on_pd=pd.DataFrame(on,columns=('Generator','Time','Value'))
# switch_pd=pd.DataFrame(switch,columns=('Generator','Time','Value'))
# srsv_pd=pd.DataFrame(srsv,columns=('Generator','Time','Value'))
# nrsv_pd=pd.DataFrame(nrsv,columns=('Generator','Time','Value'))
slack_pd = pd.DataFrame(slack,columns=('Node','Time','Value'))
flow_pd = pd.DataFrame(flow,columns=('Line','Time','Value'))
duals_pd = pd.DataFrame(duals,columns=['Constraint','Bus','Time','Value'])

#to save outputs
mwh_pd.to_csv(folder_2 + 'mwh_10ft.csv')
# vlt_angle_pd.to_csv('vlt_angle.csv')
# on_pd.to_csv('on.csv')
# switch_pd.to_csv('switch.csv')
# srsv_pd.to_csv('srsv.csv')
# nrsv_pd.to_csv('nrsv.csv')
slack_pd.to_csv(folder_2 + 'slack_10ft.csv')
flow_pd.to_csv(folder_2 + 'flow_10ft.csv')
duals_pd.to_csv(folder_2 + 'duals_10ft.csv')




