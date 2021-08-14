#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:23:59 2020

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
SrgData = pd.read_csv(SrgFile)


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

SrmDF_Daily = SrmDF_Daily[['SWC_PI_1_1_A', 'SWC_PI_1_2_A', 'P_sum']]

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

SrgDF_Daily = SrgDF_Daily[['SWC_1_1_1', 'SWC_1_2_1', 'P_sum']]

###############################################################################

###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)


lns1 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_1_1']/100),
         label = 'SRG 2 cm SWC', linestyle = '--', color = 'C1', linewidth = 4)

lns2 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_2_1']/100),
         label = 'SRG 10 cm SWC', linestyle = '--', color = 'C2', linewidth = 4)

lns3 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), (SrmDF_Daily['SWC_PI_1_1_A']/100),
         label = 'SRM 2 cm SWC', color = 'C1', linewidth = 4)

lns4 = ax1.plot(mdates.date2num(list(SrmDF_Daily.index)), (SrmDF_Daily['SWC_PI_1_2_A']/100),
         label = 'SRM 10 cm SWC', color = 'C2', linewidth = 4)

ax1.set_ylabel("Soil Moisture []", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.31, 0.1))
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.set_ylim((0, 0.4))
#ax1.margins(x=0)
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)


ax2 = ax1.twinx()
ax2.invert_yaxis()
#FufDF_Daily['P_sum'].plot(ax = ax2, label = 'Precipitation (mm)')
lns5 = ax2.bar(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['P_sum'], 
        align = 'center', label = 'SRG Precipitation [mm]', width = 2)

lns6 = ax2.bar(mdates.date2num(list(SrmDF_Daily.index)), SrmDF_Daily['P_sum'], 
        align = 'center', label = 'SRM Precipitation [mm]', width = 2)


ax2.margins(y=0)
ax2.set_ylim((90, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 41, 10))
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



plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SantaRita_Damping_Moisture_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)

















