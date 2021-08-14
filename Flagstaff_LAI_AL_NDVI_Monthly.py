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


fig = plt.figure(figsize=(20,34))
grid = gridspec.GridSpec(nrows = 4, ncols = 3)

# Add axes which can span multiple grid boxes
ax1 = fig.add_subplot(grid[0:1, 0:1], adjustable='box')
ax2 = fig.add_subplot(grid[0:1, 1:2], adjustable='box')
ax3 = fig.add_subplot(grid[0:1, 2:3], adjustable='box')
ax4 = fig.add_subplot(grid[1:2, 0:1], adjustable='box')
ax5 = fig.add_subplot(grid[1:2, 1:2], adjustable='box')
ax6 = fig.add_subplot(grid[1:2, 2:3], adjustable='box')
ax7 = fig.add_subplot(grid[2:3, 0:1], adjustable='box')
ax8 = fig.add_subplot(grid[2:3, 1:2], adjustable='box')
ax9 = fig.add_subplot(grid[2:3, 2:3], adjustable='box')
ax10 = fig.add_subplot(grid[3:4, 1:2], adjustable='box')
#ax11 = fig.add_subplot(grid[3:4, 2:3], adjustable='box')


LAIDF_AZ.groupby(['month']).mean()['FufLAI '].plot(ax=ax1, linewidth = 2, color = 'green')
LAIDF_AZ.groupby(['month']).mean()['FwfLAI '].plot(ax=ax1, linewidth = 2, color = 'red')
LAIDF_AZ.groupby(['month']).mean()['FmfLAI '].plot(ax=ax1, linewidth = 2, color = 'blue')
ax1.set_ylabel("LAI [ ]", fontsize = 18, fontweight = 'bold')
ax1.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax1.tick_params(axis='both', which='major', labelsize=18)
ax1.minorticks_off()
ax1.set_xticks(np.arange(1,13,1))
ax1.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])



ALDF_AZ.groupby(['month']).mean()['FufAL '].plot(ax=ax2, linewidth = 2, color = 'green')
ALDF_AZ.groupby(['month']).mean()['FwfAL '].plot(ax=ax2, linewidth = 2, color = 'red')
ALDF_AZ.groupby(['month']).mean()['FmfAL '].plot(ax=ax2, linewidth = 2, color = 'blue')
ax2.set_ylabel("Albedo [ ]", fontsize = 18, fontweight = 'bold')
ax2.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax2.minorticks_off()
ax2.tick_params(axis='both', which='major', labelsize=18)
ax2.set_xticks(np.arange(1,13,1))
ax2.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


NDVIDF_AZ.groupby(['month']).mean()['FufNDVI'].plot(ax=ax3, linewidth = 2, color = 'green')
NDVIDF_AZ.groupby(['month']).mean()['FwfNDVI'].plot(ax=ax3, linewidth = 2, color = 'red')
NDVIDF_AZ.groupby(['month']).mean()['FmfNDVI'].plot(ax=ax3, linewidth = 2, color = 'blue')
ax3.set_ylabel("NDVI [ ]", fontsize = 18, fontweight = 'bold')
ax3.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax3.minorticks_off()
ax3.tick_params(axis='both', which='major', labelsize=18)
ax3.set_xticks(np.arange(1,13,1))
ax3.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])




###
FufDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax4, linewidth = 2, color = 'green')
FwfDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax4, linewidth = 2, color = 'red')
FmfDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax4, linewidth = 2, color = 'blue')
ax4.set_ylabel("Net Radiation [W/$\mathregular{m^2}$]", fontsize = 18, fontweight = 'bold')
ax4.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax4.tick_params(axis='both', which='major', labelsize=18)
ax4.minorticks_off()
ax4.set_xticks(np.arange(1,13,1))
ax4.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

FufDF.groupby(['month']).mean()['LE'].plot(ax=ax5, linewidth = 2, color = 'green')
FwfDF.groupby(['month']).mean()['LE'].plot(ax=ax5, linewidth = 2, color = 'red')
FmfDF.groupby(['month']).mean()['LE'].plot(ax=ax5, linewidth = 2, color = 'blue')
ax5.set_ylabel("Latent Heat Flux [W/$\mathregular{m^2}$]", fontsize = 18, fontweight = 'bold')
ax5.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax5.minorticks_off()
#ax1.set_xticks(np.arange(1,13,1))
ax5.tick_params(axis='both', which='major', labelsize=18)
#ax2.legend(labels = line_labels, fontsize = 14)
ax5.set_xticks(np.arange(1,13,1))
ax5.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

FufDF.groupby(['month']).mean()['H'].plot(ax=ax6, linewidth = 2, color = 'green')
FwfDF.groupby(['month']).mean()['H'].plot(ax=ax6, linewidth = 2, color = 'red')
FmfDF.groupby(['month']).mean()['H'].plot(ax=ax6, linewidth = 2, color = 'blue')
ax6.set_ylabel("Sensible Heat Flux [W/$\mathregular{m^2}$]", fontsize = 18, fontweight = 'bold')
ax6.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
#ax2.set_xticks(np.arange(1,13,1))
ax6.minorticks_off()
ax6.tick_params(axis='both', which='major', labelsize=18)
#ax3.legend(labels = line_labels, fontsize = 14)
ax6.set_xticks(np.arange(1,13,1))
ax6.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

FufDF.groupby(['month']).mean()['G_1_1_1'].plot(ax=ax7, linewidth = 2, color = 'green')
FwfDF.groupby(['month']).mean()['G'].plot(ax=ax7, linewidth = 2, color = 'red')
FmfDF.groupby(['month']).mean()['G'].plot(ax=ax7, linewidth = 2, color = 'blue')
ax7.set_ylabel("Ground Heat Flux [W/$\mathregular{m^2}$]", fontsize = 18, fontweight = 'bold')
ax7.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
#ax4.set_xticks(np.arange(1,13,1))
ax7.minorticks_off()
ax7.tick_params(axis='both', which='major', labelsize=18)
#ax4.legend(labels = line_labels, fontsize = 14)
ax7.set_xticks(np.arange(1,13,1))
ax7.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

FufDF.groupby(['month']).mean()['TS_1_1_1'].plot(ax=ax8, linewidth = 2, color = 'green')
FwfDF.groupby(['month']).mean()['TS_1'].plot(ax=ax8, linewidth = 2, color = 'red')
FmfDF.groupby(['month']).mean()['TS_1'].plot(ax=ax8, linewidth = 2, color = 'blue')
ax8.set_ylabel("Surface Temperature [$^\circ$C]", fontsize = 18, fontweight = 'bold')
ax8.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax8.tick_params(axis='both', which='major', labelsize=18)
ax8.minorticks_off()
ax8.set_xticks(np.arange(1,13,1))
ax8.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

(FufDF.groupby(['month']).mean()['SWC_1_1_1'] / 100).plot(ax=ax9, linewidth = 2, color = 'green')
(FwfDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax9, linewidth = 2, color = 'red')
(FmfDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax9, linewidth = 2, color = 'blue')
ax9.set_ylabel("Soil Moisture [ ]", fontsize = 18, fontweight = 'bold')
ax9.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax9.tick_params(axis='both', which='major', labelsize=18)
ax9.minorticks_off()
ax9.set_xticks(np.arange(1,13,1))
ax9.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

FufDF.groupby(['month']).mean()['P_sum'].plot(ax=ax10, linewidth = 2, color = 'green')
FwfDF.groupby(['month']).mean()['P_sum'].plot(ax=ax10, linewidth = 2, color = 'red')
FmfDF.groupby(['month']).mean()['P_sum'].plot(ax=ax10, linewidth = 2, color = 'blue')
ax10.set_ylabel("Precipitation [mm]", fontsize = 18, fontweight = 'bold')
ax10.set_xlabel("Year", fontsize = 18, fontweight = 'bold')
ax10.tick_params(axis='both', which='major', labelsize=18)
ax10.minorticks_off()
ax10.set_xticks(np.arange(1,13,1))
ax10.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

line_labels = ["US-FUF (Control)", "US-FWF (1996 Burning)", "US-FMF (2006 Thinning)"]
handles, labels = ax9.get_legend_handles_labels()
fig.legend(handles, line_labels, loc='lower left', fontsize = 18)
#plt.show()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/Flagstaff_Monthly_Series_2.pdf", 
            bbox_inches='tight', pad_inches = 0.1,edgecolor=None)














'''
line_labels = ["US-FUF (Control)", "US-FMF (2006 Thinning)", "US-FWF (1996 Burning)"]

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(20,12))
fig.subplots_adjust(top=0.95)
#fig.suptitle('Flagstaff Monthly Average Values from 2006 to 2010', fontsize = 14, fontweight = 'bold')
FufDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax1)
FmfDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax1)
FwfDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax1)
#ax7 = ax1.twinx()
#ax7.invert_yaxis()
#FufDF.groupby(['month']).mean()['P_sum'].plot.bar(ax=ax7)
#ax7.set_ylabel('Precipitation [mm]', fontsize = 14, fontweight = 'bold')
#ax7.set_ylim((151, 0))
#ax7.margins(y=0)
ax1.set_ylabel("Net Radiation [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 16, fontweight = 'bold')
ax1.set_xticks(np.arange(1,13,1))
ax1.tick_params(axis='both', which='major', labelsize=16)
ax1.legend(labels = line_labels, fontsize = 14)
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
labels = ax1.get_xticklabels()


FufDF.groupby(['month']).mean()['LE'].plot(ax=ax2)
FmfDF.groupby(['month']).mean()['LE'].plot(ax=ax2)
FwfDF.groupby(['month']).mean()['LE'].plot(ax=ax2)
ax2.set_ylabel("Latent Heat Flux [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax2.set_xlabel("Month", fontsize = 16, fontweight = 'bold')
ax2.set_xticks(np.arange(1,13,1))
ax2.tick_params(axis='both', which='major', labelsize=16)
ax2.legend(labels = line_labels, fontsize = 14)

FufDF.groupby(['month']).mean()['H'].plot(ax=ax3)
FmfDF.groupby(['month']).mean()['H'].plot(ax=ax3)
FwfDF.groupby(['month']).mean()['H'].plot(ax=ax3)
ax3.set_ylabel("Sensible Heat Flux [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax3.set_xlabel("Month", fontsize = 16, fontweight = 'bold')
ax3.set_xticks(np.arange(1,13,1))
ax3.tick_params(axis='both', which='major', labelsize=16)
ax3.legend(labels = line_labels, fontsize = 14)

FufDF.groupby(['month']).mean()['G_1_1_1'].plot(ax=ax4)
FmfDF.groupby(['month']).mean()['G'].plot(ax=ax4)
FwfDF.groupby(['month']).mean()['G'].plot(ax=ax4)
ax4.set_ylabel("Ground Heat Flux [W/$\mathregular{m^2}$]", fontsize = 16, fontweight = 'bold')
ax4.set_xlabel("Month", fontsize = 16, fontweight = 'bold')
ax4.set_xticks(np.arange(1,13,1))
ax4.tick_params(axis='both', which='major', labelsize=16)
ax4.legend(labels = line_labels, fontsize = 14)


FufDF.groupby(['month']).mean()['TS_1_1_1'].plot(ax=ax5)
FmfDF.groupby(['month']).mean()['TS_1'].plot(ax=ax5)
FwfDF.groupby(['month']).mean()['TS_1'].plot(ax=ax5)
ax5.set_ylabel("Surface Temperature [$^\circ$C]", fontsize = 16, fontweight = 'bold')
ax5.set_xlabel("Month", fontsize = 16, fontweight = 'bold')
ax5.set_xticks(np.arange(1,13,1))
ax5.tick_params(axis='both', which='major', labelsize=16)
ax5.legend(labels = line_labels, fontsize = 14)

(FufDF.groupby(['month']).mean()['SWC_1_1_1'] / 100).plot(ax=ax6)
(FmfDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax6)
(FwfDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax6)
ax6.set_ylabel("Soil Moisture [ ]", fontsize = 16, fontweight = 'bold')
ax6.set_xlabel("Month", fontsize = 16, fontweight = 'bold')
ax6.set_xticks(np.arange(1,13,1))
ax6.tick_params(axis='both', which='major', labelsize=16)
ax6.legend(labels = line_labels, fontsize = 14)
#plt.savefig("/home/tpham/Windows Share/Thesis_Figures/FlagstaffMonthlyAverage_v2.png", 
#            bbox_inches='tight', pad_inches = 0.1)

'''















