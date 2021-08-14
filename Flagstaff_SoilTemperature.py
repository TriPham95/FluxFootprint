#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:24:09 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


FufFile = '/home/tpham/Desktop/ProcessedFiles/USFuf.csv'
FwfFile = '/home/tpham/Desktop/ProcessedFiles/USFwf.csv'


FufData = pd.read_csv(FufFile, header = 2)
FwfData = pd.read_csv(FwfFile, header = 2)



'''
FufData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufData['TIMESTAMP_START']])
FufData.set_index('Time', inplace = True, drop = True)
FufIndexStart = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200701010000]).iloc[0].name)
FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200712312330]).iloc[0].name)
#FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200712312330]).iloc[0].name)
FufData = FufData[FufIndexStart:FufIndexEnd]
FufData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FufDF_Daily = FufData

FufDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufDF_Daily['TIMESTAMP_START']])
FufDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in FufDF_Daily['day']])
FufDF_Daily = FufData.apply(pd.to_numeric).resample("D").mean()
FufDF_Daily['P_sum'] = FufData['P'].apply(pd.to_numeric).resample("D").sum()
FufDF_Daily = FufDF_Daily[['TS_1_1_1', 'TS_1_2_1', 'P_sum', 'TA']]







plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)

ax2 = ax1.twinx()
ax2.invert_yaxis()

lns1 = ax2.bar(mdates.date2num(list(FufDF_Daily.index)), FufDF_Daily['P_sum'], 
        align = 'center', label = 'FUF Precipitation [mm]', width = 2, color = 'black')

lns2 = ax1.plot(mdates.date2num(list(FufDF_Daily.index)), FufDF_Daily['TS_1_1_1'],
                label = 'Soil Temperature 2-cm [\xb0C]', linewidth = 4, color = 'peru')

lns3 = ax1.plot(mdates.date2num(list(FufDF_Daily.index)), FufDF_Daily['TS_1_2_1'],
                label = 'Soil Temperature 10-cm [\xb0C]', linewidth = 4, color = 'C1')

lns4 = ax1.plot(mdates.date2num(list(FufDF_Daily.index)), FufDF_Daily['TA'],
                label = 'Air Temperature [\xb0C]', linewidth = 4, color = 'orchid')

ax1.set_ylabel("Soil Temperature [\xb0C]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.yaxis.set_ticks(np.arange(-15, 31, 10))
ax1.set_ylim((-15, 50))
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

plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = lns3+lns2+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/FufSoilTemp_2007_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)

'''

###############################################################################
FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfData['TIMESTAMP_START']])
FwfData.set_index('Time', inplace = True, drop = True)
FwfIndexStart = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200701010000]).iloc[0].name)
FwfIndexEnd = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200712312330]).iloc[0].name)
FwfData = FwfData[FwfIndexStart:FwfIndexEnd]
FwfData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FwfDF_Daily = FwfData

FwfDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfDF_Daily['TIMESTAMP_START']])
FwfDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in FwfDF_Daily['day']])
FwfDF_Daily = FwfData.apply(pd.to_numeric).resample("D").mean()
FwfDF_Daily['P_sum'] = FwfData['P'].apply(pd.to_numeric).resample("D").sum()
FwfDF_Daily = FwfDF_Daily[['TS_1', 'TS_2', 'P_sum', 'TA']]

plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)

ax2 = ax1.twinx()
ax2.invert_yaxis()

lns1 = ax2.bar(mdates.date2num(list(FwfDF_Daily.index)), FwfDF_Daily['P_sum'], 
        align = 'center', label = 'FWF Precipitation [mm]', width = 2, color = 'black')

lns2 = ax1.plot(mdates.date2num(list(FwfDF_Daily.index)), FwfDF_Daily['TS_1'],
                label = 'Soil Temperature 2-cm [\xb0C]', linewidth = 4, color = 'peru')

lns3 = ax1.plot(mdates.date2num(list(FwfDF_Daily.index)), FwfDF_Daily['TS_2'],
                label = 'Soil Temperature 10-cm [\xb0C]', linewidth = 4, color = 'C1')

lns4 = ax1.plot(mdates.date2num(list(FwfDF_Daily.index)), FwfDF_Daily['TA'],
                label = 'Air Temperature [\xb0C]', linewidth = 4, color = 'orchid')

ax1.set_ylabel("Soil Temperature [\xb0C]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.yaxis.set_ticks(np.arange(-15, 31, 10))
ax1.set_ylim((-15, 50))
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

plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = lns4+lns3+lns2+[lns1]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=6, frameon=False)


plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/FwfSoilTemp_2007_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)























