#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:00:18 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


FufFile = '/home/tpham/Desktop/USFuf.csv'
FwfFile = '/home/tpham/Desktop/USFwf.csv'


FufData = pd.read_csv(FufFile, header = 2)
FwfData = pd.read_csv(FwfFile, header = 2)



'''
###############################################################################
FufData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufData['TIMESTAMP_START']])
FufData.set_index('Time', inplace = True, drop = True)
FufIndexStart = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200701010000]).iloc[0].name)
FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200712312330]).iloc[0].name)
#FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200712312330]).iloc[0].name)
FufData = FufData[FufIndexStart:FufIndexEnd]
FufData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FufDF_Daily = FufData

FufDF_Daily['hour'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufDF_Daily['TIMESTAMP_START']])
FufDF_Daily['hour'] = ([datetime.datetime.strftime(x, '%H') 
                        for x in FufDF_Daily['hour']])
FufDF_Daily['P_sum'] = FufData['P'].apply(pd.to_numeric).resample("H").sum()
FufDF_Daily = FufData.apply(pd.to_numeric).resample("H").mean()


FufDF_Daily = FufDF_Daily[['TS_1_1_1', 'TS_1_2_1', 'P_sum']]



FufDF_Daily['TS1_avg'] = FufDF_Daily['TS_1_1_1'].resample('D').mean()
FufDF_Daily['TS1_avg'] = FufDF_Daily['TS1_avg'].fillna(method='ffill')

FufDF_Daily['TS2_avg'] = FufDF_Daily['TS_1_2_1'].resample('D').mean()
FufDF_Daily['TS2_avg'] = FufDF_Daily['TS2_avg'].fillna(method='ffill')

FufDF_Daily['P_avg'] = FufDF_Daily['P_sum'].resample('D').sum()
#FufDF_Daily['P_avg'] = FufDF_Daily['TS2_avg'].fillna(method='ffill')

z1 = 0.02
z2 = 0.10

FufDF_Daily['DampingDepth'] = ((z1 - z2) / 
           (np.log(np.abs(FufDF_Daily['TS_1_2_1'] - FufDF_Daily['TS2_avg'])) - 
            np.log(np.abs(FufDF_Daily['TS_1_1_1'] - FufDF_Daily['TS1_avg']))))

#FufDF_Daily = FufDF_Daily[(FufDF_Daily['DampingDepth'] > 0) & (FufDF_Daily['DampingDepth'] < 50)]

FufDF_Daily['DampingDepth'][FufDF_Daily['DampingDepth'] < 0] = 0
FufDF_Daily['DampingDepth'][FufDF_Daily['DampingDepth'] > 50] = 0


FufDF_Daily = FufDF_Daily.apply(pd.to_numeric).resample("D").mean()


plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()


ax1.plot(mdates.date2num(list(FufDF_Daily.index)), FufDF_Daily['DampingDepth'],
                label = 'Damping Depth [m] - US-FUF', linewidth = 4, color = 'black')

ax2.bar(mdates.date2num(list(FufDF_Daily.index)), FufDF_Daily['P_avg'], 
        align = 'center', label = 'FWF Precipitation [mm]', width = 2, color = 'black')




ax1.minorticks_off()
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.yaxis.set_ticks(np.arange(0, 2.6, 0.5))
ax1.set_ylim((0, 4))
ax1.set_ylabel("Damping Depth [m]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')

ax1.minorticks_off()
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

ax2.margins(y=0)
ax2.set_ylim((200, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 81, 20))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))


plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USFuf_DampingDepth_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)







'''

###############################################################################
FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfData['TIMESTAMP_START']])
FwfData.set_index('Time', inplace = True, drop = True)
FwfIndexStart = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200701010000]).iloc[0].name)
FwfIndexEnd = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200712312330]).iloc[0].name)
#FwfIndexEnd = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200712312330]).iloc[0].name)
FwfData = FwfData[FwfIndexStart:FwfIndexEnd]
FwfData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FwfDF_Daily = FwfData

FwfDF_Daily['hour'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfDF_Daily['TIMESTAMP_START']])
FwfDF_Daily['hour'] = ([datetime.datetime.strftime(x, '%H') 
                        for x in FwfDF_Daily['hour']])
FwfDF_Daily['P_sum'] = FwfData['P'].apply(pd.to_numeric).resample("H").sum()
FwfDF_Daily = FwfData.apply(pd.to_numeric).resample("H").mean()

FwfDF_Daily = FwfDF_Daily[['TS_1', 'TS_2', 'P_sum']]

FwfDF_Daily['TS1_avg'] = FwfDF_Daily['TS_1'].resample('D').mean()
FwfDF_Daily['TS1_avg'] = FwfDF_Daily['TS1_avg'].fillna(method='ffill')


FwfDF_Daily['TS2_avg'] = FwfDF_Daily['TS_2'].resample('D').mean()
FwfDF_Daily['TS2_avg'] = FwfDF_Daily['TS2_avg'].fillna(method='ffill')

FwfDF_Daily['P_avg'] = FwfDF_Daily['P_sum'].resample('D').sum()

z1 = 0.02
z2 = 0.10

FwfDF_Daily['DampingDepth'] = ((z1 - z2) / 
           (np.log(np.abs(FwfDF_Daily['TS_2'] - FwfDF_Daily['TS2_avg'])) - 
            np.log(np.abs(FwfDF_Daily['TS_1'] - FwfDF_Daily['TS1_avg']))))

FwfDF_Daily['DampingDepth'][FwfDF_Daily['DampingDepth'] < 0] = 0
#FwfDF_Daily['DampingDepth'][FwfDF_Daily['DampingDepth'] > 50] = 0

FwfDF_Daily = FwfDF_Daily.apply(pd.to_numeric).resample("D").mean()





plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()


ax1.plot(mdates.date2num(list(FwfDF_Daily.index)), FwfDF_Daily['DampingDepth'],
                label = 'Damping Depth [m] - US-FWF', linewidth = 4, color = 'black')

ax2.bar(mdates.date2num(list(FwfDF_Daily.index)), FwfDF_Daily['P_avg'], 
        align = 'center', label = 'FWF Precipitation [mm]', width = 2, color = 'black')



ax1.minorticks_off()
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.yaxis.set_ticks(np.arange(0, 2.51, 0.5))
ax1.set_ylim((0, 4))
ax1.set_ylabel("Damping Depth [m]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')

ax1.minorticks_off()
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

ax2.margins(y=0)
ax2.set_ylim((200, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 81, 20))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USFwf_DampingDepth_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)


































