#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 19:40:29 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


SrgFile = '/home/tpham/Desktop/ProcessedFiles/SrgDiurnal_validation.csv'

SrgData = pd.read_csv(SrgFile)


###############################################################################
SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrgData['Date']])
SrgData.set_index('Time', inplace = True, drop = True)
SrgData.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrgData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrgData['Date']])
SrgData.drop(['Date'], axis = 1, inplace = True)
SrgData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgData['month']])
SrgData = SrgData.apply(pd.to_numeric).resample("M").mean()
SrgData['month'] = SrgData['month'].astype(int)
SrgData = SrgData.apply(pd.to_numeric).resample("M").mean()
SrgData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrgData.index])



###############################################################################
SrgFlux = '/home/tpham/Desktop/ProcessedFiles/USSrgFormatted.csv'
SrgFluxData = pd.read_csv(SrgFlux, header = 0)
SrgFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgFluxData['Timestamp']])
SrgFluxData.set_index('Time', inplace = True, drop = True)
Start = SrgFluxData.index.get_loc((SrgFluxData[SrgFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = SrgFluxData.index.get_loc((SrgFluxData[SrgFluxData['Timestamp'] == 201012312300]).iloc[0].name)
SrgFluxDF = SrgFluxData[Start:End]
SrgFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrgFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgFluxDF['Timestamp']])
SrgFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgFluxDF['month']])
SrgFluxDF['month'].astype(float)
SrgFluxDF = SrgFluxDF.apply(pd.to_numeric).resample("M").sum()
SrgFluxDF['month'] = SrgFluxDF['month'].astype(int)

SrgFluxDF = SrgFluxDF[['P_F']]
SrgFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrgFluxDF.index])


SrgParition = SrgData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

SrgParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)

SrgParition['P_F'] = SrgFluxDF['P_F']
SrgParition['Soil Evaporation'] = SrgParition['Soil Evaporation'] * 30*24
SrgParition['Wet Canopy Evaporation'] = SrgParition['Wet Canopy Evaporation'] * 30*24
SrgParition['Transpiration'] = SrgParition['Transpiration'] * 30*24
barWidth = 1
bars = np.add(SrgParition['Soil Evaporation'], SrgParition['Transpiration']).tolist()







###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()



lns2 = ax1.bar(SrgParition.index, SrgParition['Soil Evaporation'], label = 'Soil Evaporation [mm/month]',
               color='orange', width=barWidth, edgecolor = 'black',align = 'center')
lns3 = ax1.bar(SrgParition.index, SrgParition['Transpiration'], 
               bottom=SrgParition['Soil Evaporation'],  label = 'Transpiration [mm/month]',
               color='green', width=barWidth, edgecolor = 'black', align = 'center')
lns4 = ax1.bar(SrgParition.index, SrgParition['Wet Canopy Evaporation'], 
               bottom=bars, color='blue',  label = 'Wet Canopy Evaporation [mm/month]',
               width=barWidth, edgecolor = 'black', align = 'center')

lns1 = ax2.bar(SrgParition.index, SrgParition['P_F'], edgecolor = 'black', 
        align = 'center', label = 'Precipitation [mm]', width = 1)

ax1.set_ylim((0, 220))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 121, 20))
ax1.set_ylabel("ET Component [mm/month]", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)

SrgFluxDF['P_F'].plot.bar(ax=ax2, width = 1)
plt.xlim([-0.5,11.5])
#plt.xlim([0,SrgParition.size])
ax2.set_ylim((260, 0))
ax2.yaxis.set_ticks(np.arange(0, 101, 20))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')



plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = [lns4]+[lns3]+[lns2]+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SrgPartition_2010_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)


















