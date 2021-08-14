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
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates

FufFile = '/home/tpham/Desktop/ProcessedFiles/USFuf.csv'
FmfFile = '/home/tpham/Desktop/ProcessedFiles/USFmf.csv'
FwfFile = '/home/tpham/Desktop/ProcessedFiles/USFwf.csv'
LAIFile = '/home/tpham/Desktop/ProcessedFiles/LAI_AZ.csv'
ALFile = '/home/tpham/Desktop/ProcessedFiles/Albedo_AZ.csv'
NDVIFile = '/home/tpham/Desktop/ProcessedFiles/NDVI_AZ.csv'



FufData = pd.read_csv(FufFile, header = 2)
FmfData = pd.read_csv(FmfFile, header = 2)
FwfData = pd.read_csv(FwfFile, header = 2)
LAIData = pd.read_csv(LAIFile, header = 0)
ALData = pd.read_csv(ALFile, header = 0)
NDVIData = pd.read_csv(NDVIFile, header = 0)






###############################################################################
LAIData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in LAIData['Date ']])

LAIData.set_index('Time', inplace = True, drop = True)
LAIData.replace(to_replace = 'NA', value = np.nan, inplace = True) 
LAIData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in LAIData['Date ']])
LAIData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in LAIData['month']])
LAIData['month'].astype(float)
LAIDF = LAIData.apply(pd.to_numeric).resample("M").mean()
LAIDF['month'] = LAIDF['month'].astype(int)

Start = LAIDF.index.get_loc((LAIDF[LAIDF.index == '2006-01-31']).iloc[0].name)
End = LAIDF.index.get_loc((LAIDF[LAIDF.index == '2010-12-31']).iloc[0].name)
LAIDF_AZ = LAIDF[Start:End]

###############################################################################
NDVIData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in NDVIData['Date']])

NDVIData.set_index('Time', inplace = True, drop = True)
NDVIData.replace(to_replace = 'NA', value = np.nan, inplace = True) 
NDVIData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in NDVIData['Date']])
NDVIData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in NDVIData['month']])
NDVIData['month'].astype(float)
NDVIDF = NDVIData.apply(pd.to_numeric).resample("M").mean()
NDVIDF['month'] = NDVIDF['month'].astype(int)

Start = NDVIDF.index.get_loc((NDVIDF[NDVIDF.index == '2006-01-31']).iloc[0].name)
End = NDVIDF.index.get_loc((NDVIDF[NDVIDF.index == '2010-12-31']).iloc[0].name)
NDVIDF_AZ = NDVIDF[Start:End]

###############################################################################
ALData.replace(to_replace = 'NA ', value = np.nan, inplace = True) 
ALData.dropna(inplace = True)

ALData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in ALData['Date ']])

ALData.set_index('Time', inplace = True, drop = True)

ALData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in ALData['Date ']])
ALData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in ALData['month']])
ALData['month'].astype(float)
ALDF = ALData.apply(pd.to_numeric).resample("M").mean()

ALDF['month'] = ALDF['month'].astype(int)

Start = ALDF.index.get_loc((ALDF[ALDF.index == '2006-01-31']).iloc[0].name)
End = ALDF.index.get_loc((ALDF[ALDF.index == '2010-12-31']).iloc[0].name)
ALDF_AZ = ALDF[Start:End]
###############################################################################

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
FufDF['P_sum'] = FufData['P'].apply(pd.to_numeric).resample("M").sum()
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
FmfDF['P_sum'] = FmfData['P'].apply(pd.to_numeric).resample("M").sum()
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
FwfDF['P_sum'] = FwfData['P'].apply(pd.to_numeric).resample("M").sum()
FwfDF['month'] = FwfDF['month'].astype(int)
###############################################################################


fig = plt.figure(figsize=(20,16))
grid = gridspec.GridSpec(nrows = 2, ncols = 1)

# Add axes which can span multiple grid boxes
ax1 = fig.add_subplot(grid[0:1, 0:1], adjustable='box')
ax2 = fig.add_subplot(grid[1:2, 0:1], adjustable='box')

#ax11 = fig.add_subplot(grid[3:4, 2:3], adjustable='box')




FufDF.groupby(['month']).mean()['TS_1_1_1'].plot(ax=ax1, linewidth = 4, color = 'green')
FwfDF.groupby(['month']).mean()['TS_1'].plot(ax=ax1, linewidth = 4, color = 'red')
FmfDF.groupby(['month']).mean()['TS_1'].plot(ax=ax1, linewidth = 4, color = 'blue')
ax1.set_ylabel("Surface Temperature [$^\circ$C]", fontsize = 24, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax1.tick_params(axis='both', which='major', labelsize=24)
ax1.minorticks_off()
ax1.set_xticks(np.arange(1,13,1))
ax1.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

(FufDF.groupby(['month']).mean()['SWC_1_1_1'] / 100).plot(ax=ax2, linewidth = 4, color = 'green')
(FwfDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax2, linewidth = 4, color = 'red')
(FmfDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax2, linewidth = 4, color = 'blue')
ax2.set_ylabel("Soil Moisture [ ]", fontsize = 24, fontweight = 'bold')
ax2.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax2.tick_params(axis='both', which='major', labelsize=24)
ax2.minorticks_off()
ax2.set_xticks(np.arange(1,13,1))
ax2.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])



line_labels = ["US-FUF (Control)", "US-FWF (1996 Burning)", "US-FMF (2006 Thinning)"]
handles, labels = ax2.get_legend_handles_labels()
fig.legend(handles, line_labels, loc='lower center', fontsize = 24, ncol = 3)
#plt.show()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/Flagstaff_Monthly_Temp_SWC.pdf", 
            bbox_inches='tight', pad_inches = 0.1,edgecolor=None)




































