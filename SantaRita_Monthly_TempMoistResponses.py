#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:43:46 2020

@author: tpham
"""


import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates

SrcFile = '/home/tpham/Desktop/ProcessedFiles/USSrc.csv'
SrmFile = '/home/tpham/Desktop/ProcessedFiles/USSrm.csv'
SrgFile = '/home/tpham/Desktop/ProcessedFiles/USSrg.csv'
LAIFile = '/home/tpham/Desktop/ProcessedFiles/LAI_AZ.csv'
ALFile = '/home/tpham/Desktop/ProcessedFiles/Albedo_AZ.csv'
NDVIFile = '/home/tpham/Desktop/ProcessedFiles/NDVI_AZ.csv'



SrcData = pd.read_csv(SrcFile)
SrmData = pd.read_csv(SrmFile)
SrgData = pd.read_csv(SrgFile)
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

Start = LAIDF.index.get_loc((LAIDF[LAIDF.index == '2008-01-31']).iloc[0].name)
End = LAIDF.index.get_loc((LAIDF[LAIDF.index == '2014-12-31']).iloc[0].name)
LAIDF_AZ = LAIDF[Start:(End+1)]

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

Start = NDVIDF.index.get_loc((NDVIDF[NDVIDF.index == '2008-01-31']).iloc[0].name)
End = NDVIDF.index.get_loc((NDVIDF[NDVIDF.index == '2014-12-31']).iloc[0].name)
NDVIDF_AZ = NDVIDF[Start:(End+1)]

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

#ALDF.to_csv('/home/tpham/Desktop/lol.csv')

ALDF['month'] = ALDF['month'].astype(int)

Start = ALDF.index.get_loc((ALDF[ALDF.index == '2008-01-31']).iloc[0].name)
End = ALDF.index.get_loc((ALDF[ALDF.index == '2014-12-31']).iloc[0].name)
ALDF_AZ = ALDF[Start:(End+1)]
###############################################################################

###############################################################################
SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcData['TIMESTAMP_START']])
SrcData.set_index('Time', inplace = True, drop = True)
SrcData.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrcData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcData['TIMESTAMP_START']])
SrcData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcData['month']])
SrcData['month'].astype(float)
SrcDF = SrcData.apply(pd.to_numeric).resample("M").mean()
SrcDF['P_sum'] = SrcData['P'].apply(pd.to_numeric).resample("M").sum()
SrcDF['month'] = SrcDF['month'].astype(int)
###############################################################################
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData.set_index('Time', inplace = True, drop = True)
SrmData.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrmData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmData['month']])
SrmData['month'].astype(float)
SrmDF = SrmData.apply(pd.to_numeric).resample("M").mean()
SrmDF['P_sum'] = SrmData['P'].apply(pd.to_numeric).resample("M").sum()
SrmDF['month'] = SrmDF['month'].astype(int)
###############################################################################
SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData.set_index('Time', inplace = True, drop = True)
SrgData.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrgData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgData['month']])
SrmData['month'].astype(float)
SrgDF = SrgData.apply(pd.to_numeric).resample("M").mean()
SrgDF['P_sum'] = SrgData['P'].apply(pd.to_numeric).resample("M").sum()
SrgDF['month'] = SrgDF['month'].astype(int)
###############################################################################
fig = plt.figure(figsize=(20,20))
grid = gridspec.GridSpec(nrows = 2, ncols = 2)

# Add axes which can span multiple grid boxes
ax9 = fig.add_subplot(grid[0:1, 0:1], adjustable='box')
ax10 = fig.add_subplot(grid[0:1, 1:2], adjustable='box')
ax11 = fig.add_subplot(grid[1:2, 0:1], adjustable='box')
ax12 = fig.add_subplot(grid[1:2, 1:2], adjustable='box')


SrcDF.groupby(['month']).mean()['TS_1'].plot(ax=ax9, linewidth = 4, color = 'green')
SrgDF.groupby(['month']).mean()['TS_1_1_1'].plot(ax=ax9, linewidth = 4, color = 'red')
SrmDF.groupby(['month']).mean()['TS_PI_1_1_A'].plot(ax=ax9, linewidth = 4, color = 'blue')
ax9.set_ylabel("Surface Temperature [$^\circ$C]", fontsize = 24, fontweight = 'bold')
ax9.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax9.tick_params(axis='both', which='major', labelsize=24)
ax9.minorticks_off()
ax9.set_xticks(np.arange(1,13,1))
ax9.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

#SrcDF.groupby(['month']).mean()['TS_2'].plot(ax=ax10, linewidth = 4, color = 'green')
SrgDF.groupby(['month']).mean()['TS_1_6_1'].plot(ax=ax10, linewidth = 4, color = 'red')
SrmDF.groupby(['month']).mean()['TS_PI_1_8_A'].plot(ax=ax10, linewidth = 4, color = 'blue')
ax10.set_ylabel("70-cm Soil Temperature [$^\circ$C]", fontsize = 24, fontweight = 'bold')
ax10.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax10.tick_params(axis='both', which='major', labelsize=24)
ax10.minorticks_off()
ax10.set_xticks(np.arange(1,13,1))
ax10.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


(SrcDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax11, linewidth = 4, color = 'green')
(SrgDF.groupby(['month']).mean()['SWC_1_1_1'] / 100).plot(ax=ax11, linewidth = 4, color = 'red')
(SrmDF.groupby(['month']).mean()['SWC_PI_1_1_A'] / 100).plot(ax=ax11, linewidth = 4, color = 'blue')
ax11.set_ylabel("Surface Soil Moisture [ ]", fontsize = 24, fontweight = 'bold')
ax11.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax11.tick_params(axis='both', which='major', labelsize=24)
ax11.minorticks_off()
ax11.set_xticks(np.arange(1,13,1))
ax11.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])



#(SrcDF.groupby(['month']).mean()['SWC_2'] / 100).plot(ax=ax12, linewidth = 4, color = 'green')
(SrgDF.groupby(['month']).mean()['SWC_1_6_1'] / 100).plot(ax=ax12, linewidth = 4, color = 'red')
(SrmDF.groupby(['month']).mean()['SWC_PI_1_7_A'] / 100).plot(ax=ax12, linewidth = 4, color = 'blue')
ax12.set_ylabel("70-cm Moisture [ ]", fontsize = 24, fontweight = 'bold')
ax12.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax12.tick_params(axis='both', which='major', labelsize=24)
ax12.minorticks_off()
ax12.set_xticks(np.arange(1,13,1))
ax12.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


line_labels = ["US-Src (Creosote)", "US-Srg (Grassland)", "US-Srm (Mesquite)"]
handles, labels = ax9.get_legend_handles_labels()
fig.legend(handles, line_labels, loc='lower center', fontsize = 24, ncol = 3)
#plt.show()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SantaRita_Monthly_Temp_SWC.pdf", 
            bbox_inches='tight', pad_inches = 0.1,edgecolor=None)

























