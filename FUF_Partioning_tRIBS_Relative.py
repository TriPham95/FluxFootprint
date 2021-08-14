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


FufFile = '/home/tpham/Desktop/ProcessedFiles/FufDiurnal_validation.csv'

FufData = pd.read_csv(FufFile)


###############################################################################
FufData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FufData['Date']])
FufData.set_index('Time', inplace = True, drop = True)
FufData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FufData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in FufData['Date']])
FufData.drop(['Date'], axis = 1, inplace = True)
FufData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FufData['month']])
FufData = FufData.apply(pd.to_numeric).resample("M").mean()
FufData['month'] = FufData['month'].astype(int)
FufData = FufData.apply(pd.to_numeric).resample("M").mean()
FufData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FufData.index])



###############################################################################
FufFlux = '/home/tpham/Desktop/ProcessedFiles/USFufFormatted.csv'
FufFluxData = pd.read_csv(FufFlux, header = 0)
FufFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufFluxData['Timestamp']])
FufFluxData.set_index('Time', inplace = True, drop = True)
Start = FufFluxData.index.get_loc((FufFluxData[FufFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = FufFluxData.index.get_loc((FufFluxData[FufFluxData['Timestamp'] == 201012312300]).iloc[0].name)
FufFluxDF = FufFluxData[Start:End]
FufFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

FufFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufFluxDF['Timestamp']])
FufFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FufFluxDF['month']])
FufFluxDF['month'].astype(float)
FufFluxDF = FufFluxDF.apply(pd.to_numeric).resample("M").sum()
FufFluxDF['month'] = FufFluxDF['month'].astype(int)

FufFluxDF = FufFluxDF[['P']]
FufFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FufFluxDF.index])


FufParition = FufData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

FufParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)

FufParition['P'] = FufFluxDF['P']







###############################################################################
FufParition['Soil Evaporation'] = FufParition['Soil Evaporation'] * 30*24
FufParition['Wet Canopy Evaporation'] = FufParition['Wet Canopy Evaporation'] * 30*24
FufParition['Transpiration'] = FufParition['Transpiration'] * 30*24

FufParition['ET'] = FufParition['Transpiration'] + FufParition['Wet Canopy Evaporation'] + FufParition['Soil Evaporation']


FufParition['SE/ET'] = FufParition['Soil Evaporation'] / FufParition['ET']
FufParition['WCE/ET'] = FufParition['Wet Canopy Evaporation'] / FufParition['ET']
FufParition['T/ET'] = FufParition['Transpiration'] / FufParition['ET']



barWidth = 1
bars = np.add(FufParition['SE/ET'], FufParition['T/ET']).tolist()


###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()



lns2 = ax1.bar(FufParition.index, FufParition['SE/ET'], label = 'Esoil/ET',
               color='orange', width=barWidth, edgecolor = 'black',align = 'center')
lns3 = ax1.bar(FufParition.index, FufParition['T/ET'], 
               bottom=FufParition['SE/ET'],  label = 'T/ET',
               color='green', width=barWidth, edgecolor = 'black', align = 'center')
lns4 = ax1.bar(FufParition.index, FufParition['WCE/ET'], 
               bottom=bars, color='blue',  label = 'WCE/ET',
               width=barWidth, edgecolor = 'black', align = 'center')

lns1 = ax2.bar(FufParition.index, FufParition['P'], edgecolor = 'black', 
        align = 'center', label = 'Precipitation [mm]', width = 1)

ax1.set_ylim((0, 2.5))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 1.1, 0.2))
ax1.set_ylabel("Ratio of ET Component", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.2)

FufFluxDF['P'].plot.bar(ax=ax2, width = 1)
plt.xlim([-0.5,11.5])
#plt.xlim([0,FufParition.size])
ax2.set_ylim((200, 0))
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

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/FufPartition_Relative_2010_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)



















