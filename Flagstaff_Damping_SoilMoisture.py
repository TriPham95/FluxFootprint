#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:45:45 2020

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
FufDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufDF_Daily['TIMESTAMP_START']])
FufDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in FufDF_Daily['day']])
FufDF_Daily = FufData.apply(pd.to_numeric).resample("D").mean()
FufDF_Daily['P_sum'] = FufData['P'].apply(pd.to_numeric).resample("D").sum()
FufDF_Daily = FufDF_Daily[['SWC_1_1_1', 'SWC_1_2_1', 'P_sum']]


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
FwfDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfDF_Daily['TIMESTAMP_START']])
FwfDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in FwfDF_Daily['day']])
FwfDF_Daily = FwfData.apply(pd.to_numeric).resample("D").mean()
FwfDF_Daily['P_sum'] = FwfData['P'].apply(pd.to_numeric).resample("D").sum()
FwfDF_Daily = FwfDF_Daily[['SWC_1', 'SWC_2', 'P_sum']]



###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
'''
(FufDF_Daily['SWC_1_1_1']/100).plot(ax = ax1, label = 'FUF 2 cm SWC', linestyle = '--', color = 'C1', linewidth = 2)
(FufDF_Daily['SWC_1_2_1']/100).plot(ax = ax1, label = 'FUF 10 cm SWC', linestyle = '--', color = 'C2', linewidth = 2)
(FwfDF_Daily['SWC_1']/100).plot(ax = ax1, label = 'FWF 2 cm SWC', color = 'C1', linewidth = 2)
(FwfDF_Daily['SWC_2']/100).plot(ax = ax1, label = 'FWF 10 cm SWC', color = 'C2', linewidth = 2)
'''

lns1 = ax1.plot(mdates.date2num(list(FufDF_Daily.index)), (FufDF_Daily['SWC_1_1_1']/100),
         label = 'FUF 2 cm SWC', linestyle = '--', color = 'C2', linewidth = 4)

lns2 = ax1.plot(mdates.date2num(list(FufDF_Daily.index)), (FufDF_Daily['SWC_1_2_1']/100),
         label = 'FUF 10 cm SWC', color = 'C2', linewidth = 4)

lns3 = ax1.plot(mdates.date2num(list(FufDF_Daily.index)), (FwfDF_Daily['SWC_1']/100),
         label = 'FWF 2 cm SWC', linestyle = '--', color = 'C1', linewidth = 4)

lns4 = ax1.plot(mdates.date2num(list(FufDF_Daily.index)), (FwfDF_Daily['SWC_2']/100),
         label = 'FWF 10 cm SWC', color = 'C1', linewidth = 4)

ax1.set_ylabel("Soil Moisture []", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.61, 0.1))
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.set_ylim((0, 1.4))
#ax1.margins(x=0)
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)


ax2 = ax1.twinx()
ax2.invert_yaxis()
#FufDF_Daily['P_sum'].plot(ax = ax2, label = 'Precipitation (mm)')
lns5 = ax2.bar(mdates.date2num(list(FufDF_Daily.index)), FufDF_Daily['P_sum'], 
        align = 'center', label = 'FUF Precipitation [mm]', width = 2, color = 'C2')

lns6 = ax2.bar(mdates.date2num(list(FwfDF_Daily.index)), FwfDF_Daily['P_sum'], 
        align = 'center', label = 'FWF Precipitation [mm]', width = 2, 
        color = 'white', edgecolor = 'red', alpha = 0.5)


ax2.margins(y=0)
ax2.set_ylim((200, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 81, 20))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

#h1, l1 = ax1.get_legend_handles_labels()
#h2, l2 = ax2.get_legend_handles_labels()
#plt.legend(h1+h2, l1+l2, loc=2)

plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = lns1+lns2+lns3+lns4+[lns5]+[lns6]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=10, frameon=False)



plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Flagstaff_Damping_Moisture_2.png", 
            bbox_inches='tight', pad_inches = 0.1)

































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

FufDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufDF_Daily['TIMESTAMP_START']])
FufDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in FufDF_Daily['day']])
FufDF_Daily = FufData.apply(pd.to_numeric).resample("D").mean()

FufDF_Daily = FufDF_Daily[['TS_1_1_1', 'TS_1_2_1']]

FufDF_Daily['TS1_avg'] = FufDF_Daily['TS_1_1_1'].resample('M').mean()

FufDF_Daily['TS1_avg'] = FufDF_Daily['TS1_avg'].fillna(method='bfill')

FufDF_Daily['TS2_avg'] = FufDF_Daily['TS_1_2_1'].resample('M').mean()

FufDF_Daily['TS2_avg'] = FufDF_Daily['TS2_avg'].fillna(method='bfill')

z1 = 0.02
z2 = 0.10

FufDF_Daily['DampingDepth'] = ((z1 - z2) / 
           (np.log(np.abs(FufDF_Daily['TS_1_2_1'] - FufDF_Daily['TS2_avg'])) - 
            np.log(np.abs(FufDF_Daily['TS_1_1_1'] - FufDF_Daily['TS1_avg']))))

FufDF_Daily = FufDF_Daily[(FufDF_Daily['DampingDepth'] > 0)]



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

FwfDF_Daily = FwfDF_Daily[['TS_1', 'TS_2']]

FwfDF_Daily['TS1_avg'] = FwfDF_Daily['TS_1'].resample('M').mean()

FwfDF_Daily['TS1_avg'] = FwfDF_Daily['TS1_avg'].fillna(method='bfill')

FwfDF_Daily['TS2_avg'] = FwfDF_Daily['TS_2'].resample('M').mean()

FwfDF_Daily['TS2_avg'] = FwfDF_Daily['TS2_avg'].fillna(method='bfill')

z1 = 0.02
z2 = 0.10

FwfDF_Daily['DampingDepth'] = ((z1 - z2) / 
           (np.log(np.abs(FwfDF_Daily['TS_2'] - FwfDF_Daily['TS2_avg'])) - 
            np.log(np.abs(FwfDF_Daily['TS_1'] - FwfDF_Daily['TS1_avg']))))

FwfDF_Daily = FwfDF_Daily[(FwfDF_Daily['DampingDepth'] > 0)]


FwfDF_Daily['DampingDepth'].plot()




fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
FufDF_Daily['DampingDepth'].plot(ax = ax1, label = 'Control - FUF')
FwfDF_Daily['DampingDepth'].plot(ax = ax1, label = 'Severe Wildfire - FWF')
ax1.set_ylabel("Damping Depth [m]", fontsize = 14, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
#ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

labels = ax1.get_xticklabels()
ax1.legend()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Flagstaff_DampingDepth.png", 
            bbox_inches='tight', pad_inches = 0.1)
















###############################################################################

FufDF_Daily = FufData

FufDF_Daily['hour'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufDF_Daily['TIMESTAMP_START']])
FufDF_Daily['hour'] = ([datetime.datetime.strftime(x, '%H') 
                        for x in FufDF_Daily['hour']])
FufDF_Daily = FufData.apply(pd.to_numeric).resample("H").mean()

FufDF_Daily = FufDF_Daily[['TS_1_1_1', 'TS_1_2_1']]

FufDF_Daily['TS_1_1_1'] = FufDF_Daily['TS_1_1_1'].round(2)
FufDF_Daily['TS_1_2_1'] = FufDF_Daily['TS_1_2_1'].round(2)

FufDF_Daily['TS1_avg'] = FufDF_Daily['TS_1_1_1'].resample('D').mean()

FufDF_Daily['TS1_avg'] = FufDF_Daily['TS1_avg'].fillna(method='ffill')

FufDF_Daily['TS2_avg'] = FufDF_Daily['TS_1_2_1'].resample('D').mean()

FufDF_Daily['TS2_avg'] = FufDF_Daily['TS2_avg'].fillna(method='ffill')

FufDF_Daily['DampingDepth'] = ((z1 - z2) / 
           (np.log(np.abs(FufDF_Daily['TS_1_2_1'] - FufDF_Daily['TS2_avg'])) - 
            np.log(np.abs(FufDF_Daily['TS_1_1_1'] - FufDF_Daily['TS1_avg']))))


FufDF_Daily = FufDF_Daily[(FufDF_Daily['DampingDepth'] > 0) & (FufDF_Daily['DampingDepth'] < 10)]

FufDF_Daily['DampingDepth'].plot()




'''



















































































