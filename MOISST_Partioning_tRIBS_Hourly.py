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
MoisstDF = MoisstData.apply(pd.to_numeric).resample("H").mean()
MoisstDF['P_sum'] = MoisstData['Rain_Obs'].apply(pd.to_numeric).resample("H").sum()


Start = MoisstDF.index.get_loc((MoisstDF[MoisstDF.index == '2016-06-01 00:00:00']).iloc[0].name)
End = MoisstDF.index.get_loc((MoisstDF[MoisstDF.index == '2016-09-01 00:00:00']).iloc[0].name)


MoisstDF = MoisstDF[Start:(End+1)]


MoisstParition = MoisstDF[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil', 'P_sum']]

MoisstParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)




###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()



lns2 = ax1.plot(MoisstParition.index, MoisstParition['Soil Evaporation'], 
               label = 'Soil Evaporation [mm/hr]', color='orange', linewidth = 4)
lns3 = ax1.plot(MoisstParition.index, MoisstParition['Transpiration'],  
               label = 'Transpiration [mm/hr]', color='green', linewidth = 4)
lns4 = ax1.plot(MoisstParition.index, MoisstParition['Wet Canopy Evaporation'], 
               color='blue',  label = 'Wet Canopy Evaporation [mm/hr]', linewidth = 4)

lns1 = ax2.bar(MoisstParition.index, MoisstParition['P_sum'], edgecolor = 'black', 
        align = 'center', label = 'Precipitation [mm]', width = 2)

ax1.set_ylim((0, 1.6))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.81, 0.2))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 22, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)
ax2.set_ylim((80, 0))
ax2.yaxis.set_ticks(np.arange(0, 31, 10))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.set_xlabel("Date", fontsize = 22, fontweight = 'bold')
#ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))

plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)

lns = lns4+lns3+lns2+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)



plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/MoisstPartition_Hourly_2016_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)



















































