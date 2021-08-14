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



FufFile = '/home/tpham/Desktop/USFuf.csv'
FmfFile = '/home/tpham/Desktop/USFmf.csv'
FwfFile = '/home/tpham/Desktop/USFwf.csv'


FufData = pd.read_csv(FufFile, header = 2)
FmfData = pd.read_csv(FmfFile, header = 2)
FwfData = pd.read_csv(FwfFile, header = 2)

FufData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufData['TIMESTAMP_START']])
FufData.set_index('Time', inplace = True, drop = True)

FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfData['TIMESTAMP_START']])
FwfData.set_index('Time', inplace = True, drop = True)

FmfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FmfData['TIMESTAMP_START']])
FmfData.set_index('Time', inplace = True, drop = True)



FufIndexStart = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200601010000]).iloc[0].name)
FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 201012312330]).iloc[0].name)
FmfIndexStart = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200601010000]).iloc[0].name)
FmfIndexEnd = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 201012312330]).iloc[0].name)
FwfIndexStart = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200601010000]).iloc[0].name)
FwfIndexEnd = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 201012312330]).iloc[0].name)

FufDF = FufData[FufIndexStart:FufIndexEnd]
FufDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
FwfDF = FwfData[FwfIndexStart:FwfIndexEnd]
FwfDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
FmfDF = FmfData[FmfIndexStart:FmfIndexEnd]
FmfDF.replace(to_replace = -9999, value = np.nan, inplace = True)



###############################################################################
# SWC
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 12))
fig.subplots_adjust(top=0.95)
fig.suptitle('Soil Moisture Time Series at Flagstaff', 
             fontsize = 14, fontweight = 'bold')
plt.minorticks_off()
(FufDF['SWC_1_1_1'] / 100).plot(ax = ax1, color = "orange", linewidth = 0.5)
ax1.set_ylim((0, 0.8))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 0.81, 0.1))
ax1.margins(y=0)
ax1.set_ylabel("Soil Moisture (Fuf) [ ]", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
ax4 = ax1.twinx()
ax4.invert_yaxis()
FufDF['P'].plot(ax = ax4, color = "blue", linewidth = 0.5)
ax4.set_ylabel('Precipitation [mm]', fontsize = 14, fontweight = 'bold')
ax4.set_ylim((81, 0))
ax4.margins(y=0)

(FwfDF['SWC_1']/100).plot(ax = ax2, color = "orange", linewidth = 0.5)
ax2.set_ylim((0, 0.8))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(0, 0.81, 0.1))
ax2.margins(y=0)
ax2.set_ylabel("Soil Moisture (Fwf) [ ]", fontsize = 14, fontweight = 'bold')
ax2.minorticks_off()
ax5 = ax2.twinx()
ax5.invert_yaxis()
FwfDF['P'].plot(ax = ax5, color = "blue", linewidth = 0.5)
ax5.set_ylabel('Precipitation [mm]', fontsize = 14, fontweight = 'bold')
ax5.set_ylim((81, 0))
ax5.margins(y=0)

(FmfDF['SWC_1']/100).plot(ax = ax3, color = "orange", linewidth = 0.5)
ax3.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax3.set_ylim((0, 0.8))
ax3.yaxis.set_ticks(np.arange(0, 0.81, 0.1))
ax3.margins(y=0)
ax3.set_ylabel("Soil Moisture (Fmf) [ ]", fontsize = 14, fontweight = 'bold')
ax3.minorticks_off()
ax6 = ax3.twinx()
ax6.invert_yaxis()
FmfDF['P'].plot(ax = ax6, color = "blue", linewidth = 0.5)
ax6.set_ylabel('Precipitation [mm]', fontsize = 14, fontweight = 'bold')
ax3.set_xlabel('Time', fontsize = 14, fontweight = 'bold')
ax6.set_ylim((81, 0))
ax6.margins(y=0)




plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Flagstaff_SWCSeries.png", 
            bbox_inches='tight', pad_inches = 0.1)











