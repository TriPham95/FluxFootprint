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


SrmFile = '/home/tpham/Desktop/ProcessedFiles/SrmDiurnal_validation.csv'

SrmData = pd.read_csv(SrmFile)


###############################################################################
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrmData['Date']])
SrmData.set_index('Time', inplace = True, drop = True)
SrmData.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrmData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrmData['Date']])
SrmData.drop(['Date'], axis = 1, inplace = True)
SrmData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmData['month']])
SrmData = SrmData.apply(pd.to_numeric).resample("M").mean()
SrmData['month'] = SrmData['month'].astype(int)
SrmData = SrmData.apply(pd.to_numeric).resample("M").mean()
SrmData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrmData.index])



###############################################################################
SrmFlux = '/home/tpham/Desktop/ProcessedFiles/USSrmFormatted.csv'
SrmFluxData = pd.read_csv(SrmFlux, header = 0)
SrmFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmFluxData['Timestamp']])
SrmFluxData.set_index('Time', inplace = True, drop = True)
Start = SrmFluxData.index.get_loc((SrmFluxData[SrmFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = SrmFluxData.index.get_loc((SrmFluxData[SrmFluxData['Timestamp'] == 201012312300]).iloc[0].name)
SrmFluxDF = SrmFluxData[Start:End]
SrmFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrmFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmFluxDF['Timestamp']])
SrmFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmFluxDF['month']])
SrmFluxDF['month'].astype(float)
SrmFluxDF = SrmFluxDF.apply(pd.to_numeric).resample("M").sum()
SrmFluxDF['month'] = SrmFluxDF['month'].astype(int)

SrmFluxDF = SrmFluxDF[['P_F']]
SrmFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrmFluxDF.index])


SrmParition = SrmData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

SrmParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)

SrmParition['P_F'] = SrmFluxDF['P_F']
SrmParition['Soil Evaporation'] = SrmParition['Soil Evaporation'] * 30*24
SrmParition['Wet Canopy Evaporation'] = SrmParition['Wet Canopy Evaporation'] * 30*24
SrmParition['Transpiration'] = SrmParition['Transpiration'] * 30*24
barWidth = 1
bars = np.add(SrmParition['Soil Evaporation'], SrmParition['Transpiration']).tolist()







###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()



lns2 = ax1.bar(SrmParition.index, SrmParition['Soil Evaporation'], label = 'Soil Evaporation [mm/month]',
               color='orange', width=barWidth, edgecolor = 'black',align = 'center')
lns3 = ax1.bar(SrmParition.index, SrmParition['Transpiration'], 
               bottom=SrmParition['Soil Evaporation'],  label = 'Transpiration [mm/month]',
               color='green', width=barWidth, edgecolor = 'black', align = 'center')
lns4 = ax1.bar(SrmParition.index, SrmParition['Wet Canopy Evaporation'], 
               bottom=bars, color='blue',  label = 'Wet Canopy Evaporation [mm/month]',
               width=barWidth, edgecolor = 'black', align = 'center')

lns1 = ax2.bar(SrmParition.index, SrmParition['P_F'], edgecolor = 'black', 
        align = 'center', label = 'Precipitation [mm]', width = 1)

ax1.set_ylim((0, 220))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 121, 20))
ax1.set_ylabel("ET Component [mm/month]", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)

SrmFluxDF['P_F'].plot.bar(ax=ax2, width = 1)
plt.xlim([-0.5,11.5])
#plt.xlim([0,SrmParition.size])
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

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SrmPartition_2010_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)


















