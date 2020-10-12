# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from MTS_MILP import model as m1
from pyomo.core import Var
from pyomo.core import Constraint
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime
import pyomo.environ as pyo
import time

days = 3
# def sim(days):

instance = m1.create_instance('MTS_data.dat')
opt = SolverFactory("cplex")

H = instance.HorizonHours
D = 2
K=range(1,H+1)


#Space to store results
mwh=[]
on=[]
switch=[]
# srsv=[]
# nrsv=[]
vlt_angle=[]
slack = []
hydro = []

start = time.time()

#max here can be (1,365)
for day in range(1,days):
    
    for z in instance.buses:
        
        instance.HorizonHydro[z] = instance.SimHydro[z,day]
        
    #load Demand and Reserve time series data
        for i in K:
            instance.HorizonDemand[z,i] = instance.SimDemand[z,(day-1)*24+i]
            instance.HorizonSolar[z,i] = instance.SimSolar[z,(day-1)*24+i]
            
            # instance.HorizonReserves[i] = instance.SimReserves[(day-1)*24+i]
        
             
    result = opt.solve(instance,tee=True,symbolic_solver_labels=True) ##,tee=True to check number of variables\n",
    instance.solutions.load_from(result)  

 
    for v in instance.component_objects(Var, active=True):
        varobject = getattr(instance, str(v))
        a=str(v)
            
        if a=='Theta':
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    if index[0] in instance.buses:
                        vlt_angle.append((index[0],index[1]+((day-1)*24),varobject[index].value))

        if a=='S':
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    if index[0] in instance.buses:
                        slack.append((index[0],index[1]+((day-1)*24),varobject[index].value))


        if a=='H':
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    if index[0] in instance.buses:
                        hydro.append((index[0],index[1]+((day-1)*24),varobject[index].value))
                                                
                        
        if a=='mwh':
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    mwh.append((index[0],index[1]+((day-1)*24),varobject[index].value))                                            
        
        if a=='on':  
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    on.append((index[0],index[1]+((day-1)*24),varobject[index].value))

        if a=='switch':
            for index in varobject:
                if int(index[1]>0 and index[1]<25):
                    switch.append((index[0],index[1]+((day-1)*24),varobject[index].value))
                    
        # if a=='srsv':    
        #     for index in varobject:
        #         if int(index[1]>0 and index[1]<25):
        #             srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value))

        # if a=='nrsv':    
        #     for index in varobject:
        #         if int(index[1]>0 and index[1]<25):
        #             nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value))


    for j in instance.Generators:
        if instance.on[j,24] == 1:
            instance.on[j,0] = 1
        else:
            instance.on[j,0] = 0
        instance.on[j,0].fixed = True

        if instance.switch[j,24] == 1:
            instance.switch[j,0] = 1
        else:
            instance.switch[j,0] = 0
        instance.switch[j,0].fixed = True
        
    for j in instance.Generators:        
        if instance.mwh[j,24].value <=0 and instance.mwh[j,24].value>= -0.0001:
            newval_1=0
        else:
            newval_1=instance.mwh[j,24].value
        instance.mwh[j,0] = newval_1
        instance.mwh[j,0].fixed = True

            #     if instance.srsv[j,24].value <=0 and instance.srsv[j,24].value>= -0.0001:
            #         newval_srsv=0
            #     else:
            #         newval_srsv=instance.srsv[j,24].value
            #     instance.srsv[j,0] = newval_srsv
            #     instance.srsv[j,0].fixed = True

            #     if instance.nrsv[j,24].value <=0 and instance.nrsv[j,24].value>= -0.0001:
            #         newval_nrsv=0
            #     else:
            #         newval_nrsv=instance.nrsv[j,24].value
            #     instance.nrsv[j,0] = newval_nrsv
            #     instance.nrsv[j,0].fixed = True


    print(day)
        
# solar_pd=pd.DataFrame(solar,columns=('Node','Time','Value'))
# wind_pd=pd.DataFrame(wind,columns=('Node','Time','Value'))
vlt_angle_pd=pd.DataFrame(vlt_angle,columns=('Node','Time','Value'))
mwh_pd=pd.DataFrame(mwh,columns=('Generator','Time','Value'))
s_pd=pd.DataFrame(slack,columns=('Node','Time','Value'))
h_pd=pd.DataFrame(hydro,columns=('Node','Time','Value'))
on_pd=pd.DataFrame(on,columns=('Generator','Time','Value'))
switch_pd=pd.DataFrame(switch,columns=('Generator','Time','Value'))
# srsv_pd=pd.DataFrame(srsv,columns=('Generator','Time','Value'))
# nrsv_pd=pd.DataFrame(nrsv,columns=('Generator','Time','Value'))

#to save outputs
mwh_pd.to_csv('mwh.csv')
s_pd.to_csv('slack.csv')
h_pd.to_csv('hydro.csv')
# solar_pd.to_csv('solar.csv')
# wind_pd.to_csv('wind.csv')
vlt_angle_pd.to_csv('vlt_angle.csv')
on_pd.to_csv('on.csv')
switch_pd.to_csv('switch.csv')
# srsv_pd.to_csv('srsv.csv')
# nrsv_pd.to_csv('nrsv.csv')


    # return None

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)
