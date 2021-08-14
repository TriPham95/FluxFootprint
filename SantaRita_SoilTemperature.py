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



SrmFile = '/home/tpham/Desktop/ProcessedFiles/USSrm.csv'
SrgFile = '/home/tpham/Desktop/ProcessedFiles/USSrg.csv'
SrmData = pd.read_csv(SrmFile)
SrgData = pd.read_csv(SrgFile)

'''
###############################################################################
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData.set_index('Time', inplace = True, drop = True)

SrmIndexStart = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrmIndexEnd = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 200912312330]).iloc[0].name)

SrmDF = SrmData[SrmIndexStart:SrmIndexEnd]
SrmDF.replace(to_replace = -9999.0, value = np.nan, inplace = True) 

SrmDF_Daily = SrmDF

SrmDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmDF_Daily['TIMESTAMP_START']])
SrmDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in SrmDF_Daily['day']])
SrmDF_Daily = SrmData.apply(pd.to_numeric).resample("D").mean()
SrmDF_Daily['P_sum'] = SrmData['P_F'].apply(pd.to_numeric).resample("D").sum()

Start = SrmDF_Daily.index.get_loc((SrmDF_Daily[SrmDF_Daily.index == '2009-01-01']).iloc[0].name)
End = SrmDF_Daily.index.get_loc((SrmDF_Daily[SrmDF_Daily.index == '2009-12-31']).iloc[0].name)
SrmDF_Daily = SrmDF_Daily[Start:End]

SrmDF_Daily = SrmDF_Daily[['TS_PI_1_1_A', 'TS_PI_1_2_A', 
                           'TS_PI_1_3_A', 'TS_PI_1_4_A', 
                           'TS_PI_1_5_A', 'TS_PI_1_6_A', 
                           'TS_PI_1_7_A', 'TS_PI_1_8_A', 'P_sum']]




plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)


lns1 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_1_A'],
         label = 'Soil Temp 5 cm', linewidth = 4)

lns2 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_2_A'],
         label = 'Soil Temp 10 cm', linewidth = 4)

lns3 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_3_A'],
         label = 'Soil Temp 20 cm', linewidth = 4)

lns4 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_4_A'],
         label = 'Soil Temp 30 cm', linewidth = 4)

lns5 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_5_A'],
         label = 'Soil Temp 50 cm', linewidth = 4)

lns6 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_6_A'],
         label = 'Soil Temp 70 cm', linewidth = 4)

lns7 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_7_A'],
         label = 'Soil Temp 100 cm', linewidth = 4)

lns8 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['TS_PI_1_8_A'],
         label = 'Soil Temp 130 cm', linewidth = 4)


ax2 = ax1.twinx()
ax2.invert_yaxis()

lns9 = ax2.bar(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['P_sum'], 
        align = 'center', label = 'SRM Precipitation [mm]', width = 2, color = 'black')



ax1.set_ylabel("Soil Temperature [\xb0C]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()

ax1.yaxis.set_ticks(np.arange(0, 41, 10))
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.set_ylim((0, 60))
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

ax2.margins(y=0)
ax2.set_ylim((90, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 41, 10))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = lns1+lns2+lns3+lns4+lns5+lns6+lns7+lns8+[lns9]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SrmSoilTemp_2009.pdf", 
            bbox_inches='tight', pad_inches = 0.1)






'''

###############################################################################
SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData.set_index('Time', inplace = True, drop = True)

SrgIndexStart = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrgIndexEnd = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200912312330]).iloc[0].name)

SrgDF = SrgData[SrgIndexStart:SrgIndexEnd]
SrgDF.replace(to_replace = -9999.0, value = np.nan, inplace = True) 

SrgDF_Daily = SrgDF

SrgDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgDF_Daily['TIMESTAMP_START']])
SrgDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in SrgDF_Daily['day']])
SrgDF_Daily = SrgData.apply(pd.to_numeric).resample("D").mean()
SrgDF_Daily['P_sum'] = SrgData['P_F'].apply(pd.to_numeric).resample("D").sum()

Start = SrgDF_Daily.index.get_loc((SrgDF_Daily[SrgDF_Daily.index == '2009-01-01']).iloc[0].name)
End = SrgDF_Daily.index.get_loc((SrgDF_Daily[SrgDF_Daily.index == '2009-12-31']).iloc[0].name)
SrgDF_Daily = SrgDF_Daily[Start:End]

SrgDF_Daily = SrgDF_Daily[['TS_1_1_1', 'TS_1_2_1', 
                           'TS_1_3_1', 'TS_1_4_1', 
                           'TS_1_5_1', 'TS_1_6_1', 'P_sum']]


plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)




lns1 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['TS_1_1_1'],
         label = 'Soil Temp 4 cm', linewidth = 4)

lns2 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['TS_1_2_1'],
         label = 'Soil Temp 8 cm', linewidth = 4)

lns3 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['TS_1_3_1'],
         label = 'Soil Temp 18 cm', linewidth = 4)

lns4 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['TS_1_4_1'],
         label = 'Soil Temp 28 cm', linewidth = 4)

lns5 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['TS_1_5_1'],
         label = 'Soil Temp 45 cm', linewidth = 4)

lns6 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['TS_1_6_1'],
         label = 'Soil Temp 75 cm', linewidth = 4)




ax1.set_ylabel("Soil Temperature [\xb0C]", fontsize = 14, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
#ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)



ax2 = ax1.twinx()
ax2.invert_yaxis()

lns7 = ax2.bar(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['P_sum'], 
        align = 'center', label = 'SRG Precipitation [mm]', width = 2, color = 'black')



ax1.set_ylabel("Soil Temperature [\xb0C]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()

ax1.yaxis.set_ticks(np.arange(0, 41, 10))
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.set_ylim((0, 60))
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

ax2.margins(y=0)
ax2.set_ylim((90, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 41, 10))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = lns1+lns2+lns3+lns4+lns5+lns6+[lns7]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SrgSoilTemp_2009_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)

















