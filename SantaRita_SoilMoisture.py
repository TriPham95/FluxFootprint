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
from matplotlib.dates import DateFormatter



SrcFile = '/home/tpham/Desktop/USSrc.csv'
SrmFile = '/home/tpham/Desktop/USSrm.csv'
SrgFile = '/home/tpham/Desktop/USSrg.csv'


SrcData = pd.read_csv(SrcFile)
SrmData = pd.read_csv(SrmFile)
SrgData = pd.read_csv(SrgFile)

SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcData['TIMESTAMP_START']])
SrcData.set_index('Time', inplace = True, drop = True)

SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData.set_index('Time', inplace = True, drop = True)

SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData.set_index('Time', inplace = True, drop = True)



SrcIndexStart = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
SrcIndexEnd = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)
SrmIndexStart = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
SrmIndexEnd = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)
SrgIndexStart = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
SrgIndexEnd = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)

SrcDF = SrcData[SrcIndexStart:SrcIndexEnd]
SrcDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrgDF = SrgData[SrgIndexStart:SrgIndexEnd]
SrgDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrmDF = SrmData[SrmIndexStart:SrmIndexEnd]
SrmDF.replace(to_replace = -9999, value = np.nan, inplace = True)



###############################################################################
line_labels = ["Surf SWC", "Root SWC"]
# SWC
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 12))
fig.subplots_adjust(top=0.95)
fig.suptitle('Soil Moisture Time Series at Santa Rita', 
             fontsize = 14, fontweight = 'bold')
plt.minorticks_off()
(SrcDF['SWC_1'] / 100).plot(ax = ax1, color = "orange", linewidth = 0.5)
(SrcDF['SWC_2'] / 100).plot(ax = ax1, color = "green", linewidth = 0.5)
ax1.set_ylim((0, 0.3))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 0.31, 0.1))
ax1.margins(y=0)
ax1.set_ylabel("Soil Moisture (Src) [ ]", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
ax4 = ax1.twinx()
ax4.invert_yaxis()
SrcDF['P_F'].plot(ax = ax4, color = "blue", linewidth = 0.5)
ax4.set_ylabel('Precipitation [mm]', fontsize = 14, fontweight = 'bold')
ax4.set_ylim((81, 0))
ax4.margins(y=0)
ax1.legend(labels = line_labels)

(SrgDF['SWC_1_1_1']/100).plot(ax = ax2, color = "orange", linewidth = 0.5)
(SrgDF['SWC_1_6_1']/100).plot(ax = ax2, color = "green", linewidth = 0.5)
ax2.set_ylim((0, 0.3))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(0, 0.31, 0.1))
ax2.margins(y=0)
ax2.set_ylabel("Soil Moisture (Srg) [ ]", fontsize = 14, fontweight = 'bold')
ax2.minorticks_off()
ax5 = ax2.twinx()
ax5.invert_yaxis()
SrgDF['P_F'].plot(ax = ax5, color = "blue", linewidth = 0.5)
ax5.set_ylabel('Precipitation [mm]', fontsize = 14, fontweight = 'bold')
ax5.set_ylim((81, 0))
ax5.margins(y=0)
ax2.legend(labels = line_labels)

(SrmDF['SWC_PI_1_1_A']/100).plot(ax = ax3, color = "orange", linewidth = 0.5)
(SrmDF['SWC_PI_1_7_A']/100).plot(ax = ax3, color = "green", linewidth = 0.5)
ax3.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax3.set_ylim((0, 0.3))
ax3.yaxis.set_ticks(np.arange(0, 0.31, 0.1))
ax3.margins(y=0)
ax3.set_ylabel("Soil Moisture (Srm) [ ]", fontsize = 14, fontweight = 'bold')
ax3.minorticks_off()
ax6 = ax3.twinx()
ax6.invert_yaxis()
SrmDF['P_F'].plot(ax = ax6, color = "blue", linewidth = 0.5)
ax6.set_ylabel('Precipitation [mm]', fontsize = 14, fontweight = 'bold')
ax3.set_xlabel('Time', fontsize = 14, fontweight = 'bold')
ax6.set_ylim((81, 0))
ax6.margins(y=0)
ax3.legend(labels = line_labels)




plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SantaRita_SWCSeries.png", 
            bbox_inches='tight', pad_inches = 0.1)











