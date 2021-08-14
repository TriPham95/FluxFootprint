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


FwfFile = '/home/tpham/Desktop/ProcessedFiles/FwfDiurnal_calibration.csv'

FwfData = pd.read_csv(FwfFile)


###############################################################################
FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FwfData['Date']])
FwfData.set_index('Time', inplace = True, drop = True)
FwfData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FwfData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in FwfData['Date']])
FwfData.drop(['Date'], axis = 1, inplace = True)
FwfData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FwfData['month']])
FwfData = FwfData.apply(pd.to_numeric).resample("M").mean()
FwfData['month'] = FwfData['month'].astype(int)
FwfData = FwfData.apply(pd.to_numeric).resample("M").mean()
FwfData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FwfData.index])



###############################################################################
FwfFlux = '/home/tpham/Desktop/ProcessedFiles/USFwfFormatted.csv'
FwfFluxData = pd.read_csv(FwfFlux, header = 0)
FwfFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfFluxData['Timestamp']])
FwfFluxData.set_index('Time', inplace = True, drop = True)
Start = FwfFluxData.index.get_loc((FwfFluxData[FwfFluxData['Timestamp'] == 200701010000]).iloc[0].name)
End = FwfFluxData.index.get_loc((FwfFluxData[FwfFluxData['Timestamp'] == 200712312300]).iloc[0].name)
FwfFluxDF = FwfFluxData[Start:End]
FwfFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

FwfFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfFluxDF['Timestamp']])
FwfFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FwfFluxDF['month']])
FwfFluxDF['month'].astype(float)
FwfFluxDF = FwfFluxDF.apply(pd.to_numeric).resample("M").sum()
FwfFluxDF['month'] = FwfFluxDF['month'].astype(int)

FwfFluxDF = FwfFluxDF[['P']]
FwfFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FwfFluxDF.index])


FwfParition = FwfData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

FwfParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)

FwfParition['P_F'] = FwfFluxDF['P']
FwfParition['Soil Evaporation'] = FwfParition['Soil Evaporation'] * 30*24
FwfParition['Wet Canopy Evaporation'] = FwfParition['Wet Canopy Evaporation'] * 30*24
FwfParition['Transpiration'] = FwfParition['Transpiration'] * 30*24
barWidth = 1
bars = np.add(FwfParition['Soil Evaporation'], FwfParition['Transpiration']).tolist()







###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()



lns2 = ax1.bar(FwfParition.index, FwfParition['Soil Evaporation'], label = 'Soil Evaporation [mm/month]',
               color='orange', width=barWidth, edgecolor = 'black',align = 'center')
lns3 = ax1.bar(FwfParition.index, FwfParition['Transpiration'], 
               bottom=FwfParition['Soil Evaporation'],  label = 'Transpiration [mm/month]',
               color='green', width=barWidth, edgecolor = 'black', align = 'center')
lns4 = ax1.bar(FwfParition.index, FwfParition['Wet Canopy Evaporation'], 
               bottom=bars, color='blue',  label = 'Wet Canopy Evaporation [mm/month]',
               width=barWidth, edgecolor = 'black', align = 'center')

lns1 = ax2.bar(FwfParition.index, FwfParition['P_F'], edgecolor = 'black', 
        align = 'center', label = 'Precipitation [mm]', width = 1)

ax1.set_ylim((0, 300))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 161, 20))
ax1.set_ylabel("ET Component [mm/month]", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)

FwfFluxDF['P'].plot.bar(ax=ax2, width = 1)
plt.xlim([-0.5,11.5])
#plt.xlim([0,FwfParition.size])
ax2.set_ylim((240, 0))
ax2.yaxis.set_ticks(np.arange(0, 81, 20))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')



plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = [lns4]+[lns3]+[lns2]+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/FwfPartition_2007_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)


















