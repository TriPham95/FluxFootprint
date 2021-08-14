#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 10:29:41 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter



FufFile = '/home/tpham/Desktop/ProcessedFiles/USFuf.csv'
FmfFile = '/home/tpham/Desktop/ProcessedFiles/USFmf.csv'
FwfFile = '/home/tpham/Desktop/ProcessedFiles/USFwf.csv'
FufData = pd.read_csv(FufFile, header = 2)
FmfData = pd.read_csv(FmfFile, header = 2)
FwfData = pd.read_csv(FwfFile, header = 2)


###############################################################################
FufData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufData['TIMESTAMP_START']])
FufData.set_index('Time', inplace = True, drop = True)
FufData.replace(to_replace = -9999, value = np.nan, inplace = True) 
FufData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufData['TIMESTAMP_START']])
FufData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FufData['month']])
FufData['month'].astype(float)
FufDF = FufData.apply(pd.to_numeric).resample("M").mean()
FufDF['month'] = FufDF['month'].astype(int)
###############################################################################
FmfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FmfData['TIMESTAMP_START']])
FmfData.set_index('Time', inplace = True, drop = True)
FmfData.replace(to_replace = -9999, value = np.nan, inplace = True) 
FmfData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FmfData['TIMESTAMP_START']])
FmfData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FmfData['month']])
FmfData['month'].astype(float)
FmfDF = FmfData.apply(pd.to_numeric).resample("M").mean()
FmfDF['month'] = FmfDF['month'].astype(int)
###############################################################################
FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfData['TIMESTAMP_START']])
FwfData.set_index('Time', inplace = True, drop = True)
FwfData.replace(to_replace = -9999, value = np.nan, inplace = True) 
FwfData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfData['TIMESTAMP_START']])
FwfData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FwfData['month']])
FmfData['month'].astype(float)
FwfDF = FwfData.apply(pd.to_numeric).resample("M").mean()
FwfDF['month'] = FwfDF['month'].astype(int)
###############################################################################




line_labels = ["US-FUF (Control)", "US-FWF (1996 Burning)"]

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(20,12))
fig.subplots_adjust(top=0.95)
#fig.suptitle('Flagstaff Monthly Average Values from 2006 to 2010', fontsize = 16, fontweight = 'bold')

FufDF['NETRAD'].plot(ax=ax1)
FwfDF['NETRAD'].plot(ax=ax1)
ax1.set_ylabel("Net Radiation [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax1.set_xlabel("Year", fontsize = 16, fontweight = 'bold')
#ax1.set_xticks(np.arange(1,13,1))
ax1.tick_params(axis='both', which='major', labelsize=16)
ax1.minorticks_off()
#ax1.legend(labels = line_labels, fontsize = 14)

FufDF['LE'].plot(ax=ax2)
FwfDF['LE'].plot(ax=ax2)
ax2.set_ylabel("Latent Heat Flux [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax2.set_xlabel("Year", fontsize = 16, fontweight = 'bold')
ax2.minorticks_off()
#ax1.set_xticks(np.arange(1,13,1))
ax2.tick_params(axis='both', which='major', labelsize=16)
#ax2.legend(labels = line_labels, fontsize = 14)

FufDF['H'].plot(ax=ax3)
FwfDF['H'].plot(ax=ax3)
ax3.set_ylabel("Sensible Heat Flux [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax3.set_xlabel("Year", fontsize = 16, fontweight = 'bold')
#ax2.set_xticks(np.arange(1,13,1))
ax3.minorticks_off()
ax3.tick_params(axis='both', which='major', labelsize=16)
#ax3.legend(labels = line_labels, fontsize = 14)

FufDF['G_1_1_1'].plot(ax=ax4)
FwfDF['G'].plot(ax=ax4)
ax4.set_ylabel("Ground Heat Flux [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax4.set_xlabel("Year", fontsize = 16, fontweight = 'bold')
#ax4.set_xticks(np.arange(1,13,1))
ax4.minorticks_off()
ax4.tick_params(axis='both', which='major', labelsize=16)
#ax4.legend(labels = line_labels, fontsize = 14)

FufDF['TS_1_1_1'].plot(ax=ax5)
FwfDF['TS_1'].plot(ax=ax5)
ax5.set_ylabel("Surface Temperature [$^\circ$C]", fontsize = 16, fontweight = 'bold')
ax5.set_xlabel("Year", fontsize = 16, fontweight = 'bold')
ax5.tick_params(axis='both', which='major', labelsize=16)
#ax5.set_xticks(np.arange(1,13,1))
ax5.minorticks_off()
#ax5.legend(labels = line_labels, fontsize = 14)

(FufDF['SWC_1_1_1'] / 100).plot(ax=ax6)
(FwfDF['SWC_1'] / 100).plot(ax=ax6)
ax6.set_ylabel("Soil Moisture [ ]", fontsize = 16, fontweight = 'bold')
ax6.set_xlabel("Year", fontsize = 16, fontweight = 'bold')
ax6.tick_params(axis='both', which='major', labelsize=16)
#ax6.set_xticks(np.arange(1,13,1))
ax6.minorticks_off()
#ax6.legend(labels = line_labels, fontsize = 14)

#plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SevereFireComparison.png", 
#            bbox_inches='tight', pad_inches = 0.1,edgecolor=None)



















#ax = FufDF.boxplot(column=['LE'], by = 'month')
#ax.grid(False)












