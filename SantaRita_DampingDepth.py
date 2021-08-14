#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:51:15 2020

@author: tpham
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 11:07:54 2019

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates



SrmFile = '/home/tpham/Desktop/USSrm.csv'
SrgFile = '/home/tpham/Desktop/Tribs_USSrg_20082014/USSrg.csv'
SrmData = pd.read_csv(SrmFile)


###############################################################################
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData.set_index('Time', inplace = True, drop = True)

SrmIndexStart = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrmIndexEnd = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 200912312330]).iloc[0].name)

SrmDF = SrmData[SrmIndexStart:SrmIndexEnd]
SrmDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrmDF_Daily = SrmDF

SrmDF_Daily['hour'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmDF_Daily['TIMESTAMP_START']])
SrmDF_Daily['hour'] = ([datetime.datetime.strftime(x, '%H') 
                        for x in SrmDF_Daily['hour']])

SrmDF_Daily = SrmData.apply(pd.to_numeric).resample("H").mean()
SrmDF_Daily['P_sum'] = SrmDF['P_F'].apply(pd.to_numeric).resample("H").sum()



Start = SrmDF_Daily.index.get_loc((SrmDF_Daily[SrmDF_Daily.index == '2009-01-01 00:00:00']).iloc[0].name)
End = SrmDF_Daily.index.get_loc((SrmDF_Daily[SrmDF_Daily.index == '2009-12-31 23:00:00']).iloc[0].name)
SrmDF_Daily = SrmDF_Daily[Start:End]

SrmDF_Daily = SrmDF_Daily[['TS_PI_1_1_A', 'TS_PI_1_2_A', 'TS_PI_1_5_A', 'P_sum']]




SrmDF_Daily['TSS_avg'] = SrmDF_Daily['TS_PI_1_1_A'].resample('D').mean()

SrmDF_Daily['TSS_avg'] = SrmDF_Daily['TSS_avg'].fillna(method='ffill')

SrmDF_Daily['TSS2_avg'] = SrmDF_Daily['TS_PI_1_2_A'].resample('D').mean()

SrmDF_Daily['TSS2_avg'] = SrmDF_Daily['TSS2_avg'].fillna(method='ffill')

SrmDF_Daily['P_avg'] = SrmDF_Daily['P_sum'].resample('D').sum()

z1 = 0.05
z2 = 0.1

SrmDF_Daily['DampingDepth'] = ((z1 - z2) / 
           (np.log(np.abs(SrmDF_Daily['TS_PI_1_2_A'] - SrmDF_Daily['TSS2_avg'])) - 
            np.log(np.abs(SrmDF_Daily['TS_PI_1_1_A'] - SrmDF_Daily['TSS_avg']))))

SrmDF_Daily['DampingDepth'][SrmDF_Daily['DampingDepth'] < 0] = 0
SrmDF_Daily['DampingDepth'][SrmDF_Daily['DampingDepth'] > 20] = 0

SrmDF_Daily = SrmDF_Daily.apply(pd.to_numeric).resample("D").mean()




plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()


ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['DampingDepth'],
                label = 'Damping Depth [m] - US-SRM', linewidth = 4, color = 'black')

ax2.bar(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['P_avg'], 
        align = 'center', label = 'SRM Precipitation [mm]', width = 2, color = 'black')




ax1.minorticks_off()
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.yaxis.set_ticks(np.arange(0, 2.1, 0.5))
ax1.set_ylim((0, 3))
ax1.set_ylabel("Damping Depth [m]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')

ax1.minorticks_off()
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

ax2.margins(y=0)
ax2.set_ylim((50, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 31, 10))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USSrm_DampingDepth_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)


'''



###############################################################################
SrgData = pd.read_csv(SrgFile)

SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData.set_index('Time', inplace = True, drop = True)

SrgIndexStart = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrgIndexEnd = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200912312330]).iloc[0].name)

SrgDF = SrgData[SrgIndexStart:SrgIndexEnd]
SrgDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrgDF_Daily = SrgDF

SrgDF_Daily['hour'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgDF_Daily['TIMESTAMP_START']])
SrgDF_Daily['hour'] = ([datetime.datetime.strftime(x, '%H') 
                        for x in SrgDF_Daily['hour']])

SrgDF_Daily = SrgData.apply(pd.to_numeric).resample("H").mean()
SrgDF_Daily['P_sum'] = SrgDF['P_F'].apply(pd.to_numeric).resample("H").sum()



Start = SrgDF_Daily.index.get_loc((SrgDF_Daily[SrgDF_Daily.index == '2009-01-01 00:00:00']).iloc[0].name)
End = SrgDF_Daily.index.get_loc((SrgDF_Daily[SrgDF_Daily.index == '2009-12-31 23:00:00']).iloc[0].name)
SrgDF_Daily = SrgDF_Daily[Start:End]

SrgDF_Daily = SrgDF_Daily[['TS_1_1_1', 'TS_1_2_1', 'TS_1_4_1', 'P_sum']]



SrgDF_Daily['P_avg'] = SrgDF_Daily['P_sum'].resample('D').sum()

SrgDF_Daily['TSS_avg'] = SrgDF_Daily['TS_1_1_1'].resample('D').mean()

SrgDF_Daily['TSS_avg'] = SrgDF_Daily['TSS_avg'].fillna(method='ffill')

SrgDF_Daily['TSS2_avg'] = SrgDF_Daily['TS_1_2_1'].resample('D').mean()

SrgDF_Daily['TSS2_avg'] = SrgDF_Daily['TSS_avg'].fillna(method='ffill')


z1 = 0.04
z2 = 0.08

SrgDF_Daily['DampingDepth'] = ((z1 - z2) / 
           (np.log(np.abs(SrgDF_Daily['TS_1_2_1'] - SrgDF_Daily['TSS2_avg'])) - 
            np.log(np.abs(SrgDF_Daily['TS_1_1_1'] - SrgDF_Daily['TSS_avg']))))

SrgDF_Daily['DampingDepth'][SrgDF_Daily['DampingDepth'] < 0] = 0
SrgDF_Daily['DampingDepth'][SrgDF_Daily['DampingDepth'] > 10] = 0

SrgDF_Daily = SrgDF_Daily.apply(pd.to_numeric).resample("D").mean()



plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)
ax2 = ax1.twinx()
ax2.invert_yaxis()


ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['DampingDepth'],
                label = 'Damping Depth [m] - US-SRG', linewidth = 4, color = 'black')

ax2.bar(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['P_avg'], 
        align = 'center', label = 'SRG Precipitation [mm]', width = 2, color = 'black')

ax1.minorticks_off()
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.yaxis.set_ticks(np.arange(0, 0.61, 0.1))
ax1.set_ylim((0, 1.2))
ax1.set_ylabel("Damping Depth [m]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')

ax1.minorticks_off()
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

ax2.margins(y=0)
ax2.set_ylim((60, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 31, 10))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))





plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USSrg_DampingDepth_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)


'''





































