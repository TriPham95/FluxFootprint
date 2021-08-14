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


SrcFile = '/home/tpham/Desktop/ProcessedFiles/SrcDiurnal_validation.csv'

SrcData = pd.read_csv(SrcFile)


###############################################################################
SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrcData['Date']])
SrcData.set_index('Time', inplace = True, drop = True)
SrcData.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrcData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrcData['Date']])
SrcData.drop(['Date'], axis = 1, inplace = True)
SrcData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcData['month']])
SrcData = SrcData.apply(pd.to_numeric).resample("M").mean()
SrcData['month'] = SrcData['month'].astype(int)
SrcData = SrcData.apply(pd.to_numeric).resample("M").mean()
SrcData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrcData.index])



###############################################################################
SrcFlux = '/home/tpham/Desktop/ProcessedFiles/USSrcFormatted.csv'
SrcFluxData = pd.read_csv(SrcFlux, header = 0)
SrcFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcFluxData['Timestamp']])
SrcFluxData.set_index('Time', inplace = True, drop = True)
Start = SrcFluxData.index.get_loc((SrcFluxData[SrcFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = SrcFluxData.index.get_loc((SrcFluxData[SrcFluxData['Timestamp'] == 201012312300]).iloc[0].name)
SrcFluxDF = SrcFluxData[Start:End]
SrcFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrcFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcFluxDF['Timestamp']])
SrcFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcFluxDF['month']])
SrcFluxDF['month'].astype(float)
SrcFluxDF = SrcFluxDF.apply(pd.to_numeric).resample("M").sum()
SrcFluxDF['month'] = SrcFluxDF['month'].astype(int)

SrcFluxDF = SrcFluxDF[['P_F']]
SrcFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrcFluxDF.index])


SrcParition = SrcData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

SrcParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)

SrcParition['P_F'] = SrcFluxDF['P_F']







###############################################################################
SrcParition['Soil Evaporation'] = SrcParition['Soil Evaporation'] * 30*24
SrcParition['Wet Canopy Evaporation'] = SrcParition['Wet Canopy Evaporation'] * 30*24
SrcParition['Transpiration'] = SrcParition['Transpiration'] * 30*24

SrcParition['ET'] = SrcParition['Transpiration'] + SrcParition['Wet Canopy Evaporation'] + SrcParition['Soil Evaporation']


SrcParition['SE/ET'] = SrcParition['Soil Evaporation'] / SrcParition['ET']
SrcParition['WCE/ET'] = SrcParition['Wet Canopy Evaporation'] / SrcParition['ET']
SrcParition['T/ET'] = SrcParition['Transpiration'] / SrcParition['ET']



barWidth = 1
bars = np.add(SrcParition['SE/ET'], SrcParition['T/ET']).tolist()


###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()



lns2 = ax1.bar(SrcParition.index, SrcParition['SE/ET'], label = 'Esoil/ET',
               color='orange', width=barWidth, edgecolor = 'black',align = 'center')
lns3 = ax1.bar(SrcParition.index, SrcParition['T/ET'], 
               bottom=SrcParition['SE/ET'],  label = 'T/ET',
               color='green', width=barWidth, edgecolor = 'black', align = 'center')
lns4 = ax1.bar(SrcParition.index, SrcParition['WCE/ET'], 
               bottom=bars, color='blue',  label = 'WCE/ET',
               width=barWidth, edgecolor = 'black', align = 'center')

lns1 = ax2.bar(SrcParition.index, SrcParition['P_F'], edgecolor = 'black', 
        align = 'center', label = 'Precipitation [mm]', width = 1)

ax1.set_ylim((0, 2.5))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 1.1, 0.2))
ax1.set_ylabel("Ratio of ET Component", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.2)

SrcFluxDF['P_F'].plot.bar(ax=ax2, width = 1)
plt.xlim([-0.5,11.5])
#plt.xlim([0,SrcParition.size])
ax2.set_ylim((160, 0))
ax2.yaxis.set_ticks(np.arange(0, 61, 10))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')



plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = [lns4]+[lns3]+[lns2]+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SrcPartition_Relative_2010_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)



















