#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 09:34:53 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates



SrgFile = '/home/tpham/Desktop/ProcessedFiles/USSrg.csv'
SrgData = pd.read_csv(SrgFile)


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

SrgDF_Daily = SrgDF_Daily[['SWC_1_1_1', 'SWC_1_2_1', 'SWC_1_3_1', 
                           'SWC_1_4_1', 'SWC_1_5_1', 'SWC_1_6_1',
                           'P_sum']]



###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)


lns1 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_1_1']/100),
         label = 'SRG 5 cm SWC', linewidth = 4)

lns2 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_2_1']/100),
         label = 'SRG 10 cm SWC', linewidth = 4)

lns3 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_3_1']/100),
         label = 'SRG 20 cm SWC', linewidth = 4)

lns4 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_4_1']/100),
         label = 'SRG 30 cm SWC', linewidth = 4)

lns5 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_5_1']/100),
         label = 'SRG 45 cm SWC', linewidth = 4)

lns6 = ax1.plot(mdates.date2num(list(SrgDF_Daily.index)), (SrgDF_Daily['SWC_1_6_1']/100),
         label = 'SRG 75 cm SWC', linewidth = 4)





ax1.set_ylabel("Soil Moisture []", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.26, 0.05))
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

lns7 = ax2.bar(mdates.date2num(list(SrgDF_Daily.index)), SrgDF_Daily['P_sum'], 
        align = 'center', label = 'SRG Precipitation [mm]', width = 2, color = 'black')


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


lns = lns1+lns2+lns3+lns4+lns5+lns6+[lns7]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=1, frameon=False)



plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SRG_Moisture_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)


























