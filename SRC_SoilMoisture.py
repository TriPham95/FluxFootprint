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



SrcFile = '/home/tpham/Desktop/ProcessedFiles/USSrc.csv'
SrcData = pd.read_csv(SrcFile)


###############################################################################
SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcData['TIMESTAMP_START']])
SrcData.set_index('Time', inplace = True, drop = True)

SrcIndexStart = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrcIndexEnd = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 200912312330]).iloc[0].name)

SrcDF = SrcData[SrcIndexStart:SrcIndexEnd]
SrcDF.replace(to_replace = -9999.0, value = np.nan, inplace = True) 

SrcDF_Daily = SrcDF

SrcDF_Daily['day'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcDF_Daily['TIMESTAMP_START']])
SrcDF_Daily['day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in SrcDF_Daily['day']])
SrcDF_Daily = SrcData.apply(pd.to_numeric).resample("D").mean()
SrcDF_Daily['P_sum'] = SrcData['P_F'].apply(pd.to_numeric).resample("D").sum()

Start = SrcDF_Daily.index.get_loc((SrcDF_Daily[SrcDF_Daily.index == '2009-01-01']).iloc[0].name)
End = SrcDF_Daily.index.get_loc((SrcDF_Daily[SrcDF_Daily.index == '2009-12-31']).iloc[0].name)
SrcDF_Daily = SrcDF_Daily[Start:End]

SrcDF_Daily = SrcDF_Daily[['SWC_1', 'SWC_2', 'P_sum']]



###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)


lns1 = ax1.plot(mdates.date2num(list(SrcDF_Daily.index)), (SrcDF_Daily['SWC_1']/100),
         label = 'Src 2.5 cm SWC', linewidth = 4)

lns2 = ax1.plot(mdates.date2num(list(SrcDF_Daily.index)), (SrcDF_Daily['SWC_2']/100),
         label = 'Src 12.5 cm SWC', linewidth = 4)






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

lns7 = ax2.bar(mdates.date2num(list(SrcDF_Daily.index)), SrcDF_Daily['P_sum'], 
        align = 'center', label = 'SRC Precipitation [mm]', width = 2, color = 'black')


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


lns = lns1+lns2+[lns7]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=7, frameon=False)



plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SRC_Moisture_v2.pdf", 
            bbox_inches='tight', pad_inches = 0.1)


























