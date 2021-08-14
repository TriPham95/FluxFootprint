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


MoisstFile = '/home/tpham/Desktop/ProcessedFiles/MoisstDiurnal_calibration.csv'

MoisstData = pd.read_csv(MoisstFile)


###############################################################################
MoisstData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in MoisstData['Date']])
MoisstData.set_index('Time', inplace = True, drop = True)
MoisstData.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in MoisstData['Date']])
MoisstData.drop(['Date'], axis = 1, inplace = True)
MoisstData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in MoisstData['month']])
MoisstData['month'] = MoisstData['month'].astype(int)
MoisstDF = MoisstData.apply(pd.to_numeric).resample("M").mean()
MoisstDF['P_sum'] = MoisstData['Rain_Obs'].apply(pd.to_numeric).resample("M").sum()



MoisstDF['month'] = MoisstData['month'].astype(int)



MoisstDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in MoisstDF.index])



MoisstParition = MoisstDF[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil', 'P_sum']]

MoisstParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)





###############################################################################
MoisstParition['Soil Evaporation'] = MoisstParition['Soil Evaporation'] * 30*24
MoisstParition['Wet Canopy Evaporation'] = MoisstParition['Wet Canopy Evaporation'] * 30*24
MoisstParition['Transpiration'] = MoisstParition['Transpiration'] * 30*24

MoisstParition['ET'] = MoisstParition['Transpiration'] + MoisstParition['Wet Canopy Evaporation'] + MoisstParition['Soil Evaporation']


MoisstParition['SE/ET'] = MoisstParition['Soil Evaporation'] / MoisstParition['ET']
MoisstParition['WCE/ET'] = MoisstParition['Wet Canopy Evaporation'] / MoisstParition['ET']
MoisstParition['T/ET'] = MoisstParition['Transpiration'] / MoisstParition['ET']



barWidth = 1
bars = np.add(MoisstParition['SE/ET'], MoisstParition['T/ET']).tolist()


###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()



lns2 = ax1.bar(MoisstParition.index, MoisstParition['SE/ET'], label = 'Esoil/ET',
               color='orange', width=barWidth, edgecolor = 'black',align = 'center')
lns3 = ax1.bar(MoisstParition.index, MoisstParition['T/ET'], 
               bottom=MoisstParition['SE/ET'],  label = 'T/ET',
               color='green', width=barWidth, edgecolor = 'black', align = 'center')
lns4 = ax1.bar(MoisstParition.index, MoisstParition['WCE/ET'], 
               bottom=bars, color='blue',  label = 'WCE/ET',
               width=barWidth, edgecolor = 'black', align = 'center')

lns1 = ax2.bar(MoisstParition.index, MoisstParition['P_sum'], edgecolor = 'black', 
        align = 'center', label = 'Precipitation [mm]', width = 1)

ax1.set_ylim((0, 2.7))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 1.1, 0.2))
ax1.set_ylabel("Ratio of ET Component", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.2)


plt.xlim([-0.5,11.5])
#plt.xlim([0,MoisstParition.size])
ax2.set_ylim((380, 0))
ax2.yaxis.set_ticks(np.arange(0, 161, 40))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')



plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = [lns4]+[lns3]+[lns2]+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/MoisstPartition_Relative_2016_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)



















