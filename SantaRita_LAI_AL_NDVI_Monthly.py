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
fig = plt.figure(figsize=(40,22))
grid = gridspec.GridSpec(nrows = 3, ncols = 4)

# Add axes which can span multiple grid boxes
ax1 = fig.add_subplot(grid[0:1, 0:1], adjustable='box')
ax2 = fig.add_subplot(grid[0:1, 1:2], adjustable='box')
ax3 = fig.add_subplot(grid[0:1, 2:3], adjustable='box')
ax4 = fig.add_subplot(grid[0:1, 3:4], adjustable='box')
ax5 = fig.add_subplot(grid[1:2, 0:1], adjustable='box')
ax6 = fig.add_subplot(grid[1:2, 1:2], adjustable='box')
ax7 = fig.add_subplot(grid[1:2, 2:3], adjustable='box')
ax8 = fig.add_subplot(grid[1:2, 3:4], adjustable='box')
ax9 = fig.add_subplot(grid[2:3, 0:1], adjustable='box')
ax10 = fig.add_subplot(grid[2:3, 1:2], adjustable='box')
ax11 = fig.add_subplot(grid[2:3, 2:3], adjustable='box')
ax12 = fig.add_subplot(grid[2:3, 3:4], adjustable='box')



SrcDF.groupby(['month']).mean()['P_sum'].plot(ax=ax1, linewidth = 2, color = 'green')
SrgDF.groupby(['month']).mean()['P_sum'].plot(ax=ax1, linewidth = 2, color = 'red')
SrmDF.groupby(['month']).mean()['P_sum'].plot(ax=ax1, linewidth = 2, color = 'blue')
ax1.set_ylabel("Precipitation [mm]", fontsize = 26, fontweight = 'bold')
ax1.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax1.tick_params(axis='both', which='major', labelsize=26)
ax1.minorticks_off()
ax1.set_xticks(np.arange(1,13,1))
ax1.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


LAIDF_AZ.groupby(['month']).mean()['SrcLAI '].plot(ax=ax2, linewidth = 2, color = 'green')
LAIDF_AZ.groupby(['month']).mean()['SrgLAI '].plot(ax=ax2, linewidth = 2, color = 'red')
LAIDF_AZ.groupby(['month']).mean()['SrmLAI'].plot(ax=ax2, linewidth = 2, color = 'blue')
ax2.set_ylabel("LAI [ ]", fontsize = 26, fontweight = 'bold')
ax2.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax2.tick_params(axis='both', which='major', labelsize=26)
ax2.minorticks_off()
ax2.set_xticks(np.arange(1,13,1))
ax2.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


ALDF_AZ.groupby(['month']).mean()['SrcAL '].plot(ax=ax3, linewidth = 2, color = 'green')
ALDF_AZ.groupby(['month']).mean()['SrgAL '].plot(ax=ax3, linewidth = 2, color = 'red')
ALDF_AZ.groupby(['month']).mean()['SrmAL'].plot(ax=ax3, linewidth = 2, color = 'blue')
ax3.set_ylabel("Albedo [ ]", fontsize = 26, fontweight = 'bold')
ax3.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax3.minorticks_off()
ax3.tick_params(axis='both', which='major', labelsize=26)
ax3.set_xticks(np.arange(1,13,1))
ax3.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


NDVIDF_AZ.groupby(['month']).mean()['SrcNDVI'].plot(ax=ax4, linewidth = 2, color = 'green')
NDVIDF_AZ.groupby(['month']).mean()['SrgNDVI'].plot(ax=ax4, linewidth = 2, color = 'red')
NDVIDF_AZ.groupby(['month']).mean()['SrmNDVI'].plot(ax=ax4, linewidth = 2, color = 'blue')
ax4.set_ylabel("NDVI [ ]", fontsize = 26, fontweight = 'bold')
ax4.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax4.minorticks_off()
ax4.tick_params(axis='both', which='major', labelsize=26)
ax4.set_xticks(np.arange(1,13,1))
ax4.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

###
SrcDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax5, linewidth = 2, color = 'green')
SrgDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax5, linewidth = 2, color = 'red')
SrmDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax5, linewidth = 2, color = 'blue')
ax5.set_ylabel("Net Radiation [W/$\mathregular{m^2}$]", fontsize = 26, fontweight = 'bold')
ax5.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax5.tick_params(axis='both', which='major', labelsize=26)
ax5.minorticks_off()
ax5.set_xticks(np.arange(1,13,1))
ax5.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

SrcDF.groupby(['month']).mean()['LE_F_MDS'].plot(ax=ax6, linewidth = 2, color = 'green')
SrgDF.groupby(['month']).mean()['LE_F_MDS'].plot(ax=ax6, linewidth = 2, color = 'red')
SrmDF.groupby(['month']).mean()['LE_F_MDS'].plot(ax=ax6, linewidth = 2, color = 'blue')
ax6.set_ylabel("Latent Heat Flux [W/$\mathregular{m^2}$]", fontsize = 26, fontweight = 'bold')
ax6.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax6.minorticks_off()
ax6.tick_params(axis='both', which='major', labelsize=26)
ax6.set_xticks(np.arange(1,13,1))
ax6.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

SrcDF.groupby(['month']).mean()['H_F_MDS'].plot(ax=ax7, linewidth = 2, color = 'green')
SrgDF.groupby(['month']).mean()['H_F_MDS'].plot(ax=ax7, linewidth = 2, color = 'red')
SrmDF.groupby(['month']).mean()['H_F_MDS'].plot(ax=ax7, linewidth = 2, color = 'blue')
ax7.set_ylabel("Sensible Heat Flux [W/$\mathregular{m^2}$]", fontsize = 26, fontweight = 'bold')
ax7.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax7.minorticks_off()
ax7.tick_params(axis='both', which='major', labelsize=26)
ax7.set_xticks(np.arange(1,13,1))
ax7.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

SrcDF.groupby(['month']).mean()['G_F_MDS'].plot(ax=ax8, linewidth = 2, color = 'green')
SrgDF.groupby(['month']).mean()['G_F_MDS'].plot(ax=ax8, linewidth = 2, color = 'red')
SrmDF.groupby(['month']).mean()['G_F_MDS'].plot(ax=ax8, linewidth = 2, color = 'blue')
ax8.set_ylabel("Ground Heat Flux [W/$\mathregular{m^2}$]", fontsize = 26, fontweight = 'bold')
ax8.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
#ax4.set_xticks(np.arange(1,13,1))
ax8.minorticks_off()
ax8.tick_params(axis='both', which='major', labelsize=26)
#ax4.legend(labels = line_labels, fontsize = 14)
ax8.set_xticks(np.arange(1,13,1))
ax8.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

SrcDF.groupby(['month']).mean()['TS_1'].plot(ax=ax9, linewidth = 2, color = 'green')
SrgDF.groupby(['month']).mean()['TS_1_1_1'].plot(ax=ax9, linewidth = 2, color = 'red')
SrmDF.groupby(['month']).mean()['TS_PI_1_1_A'].plot(ax=ax9, linewidth = 2, color = 'blue')
ax9.set_ylabel("Surface Temperature [$^\circ$C]", fontsize = 26, fontweight = 'bold')
ax9.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax9.tick_params(axis='both', which='major', labelsize=26)
ax9.minorticks_off()
ax9.set_xticks(np.arange(1,13,1))
ax9.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

SrcDF.groupby(['month']).mean()['TS_2'].plot(ax=ax10, linewidth = 2, color = 'green')
SrgDF.groupby(['month']).mean()['TS_1_6_1'].plot(ax=ax10, linewidth = 2, color = 'red')
SrmDF.groupby(['month']).mean()['TS_PI_1_8_A'].plot(ax=ax10, linewidth = 2, color = 'blue')
ax10.set_ylabel("Rootzone Temperature [$^\circ$C]", fontsize = 26, fontweight = 'bold')
ax10.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax10.tick_params(axis='both', which='major', labelsize=26)
ax10.minorticks_off()
ax10.set_xticks(np.arange(1,13,1))
ax10.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


(SrcDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax11, linewidth = 2, color = 'green')
(SrgDF.groupby(['month']).mean()['SWC_1_1_1'] / 100).plot(ax=ax11, linewidth = 2, color = 'red')
(SrmDF.groupby(['month']).mean()['SWC_PI_1_1_A'] / 100).plot(ax=ax11, linewidth = 2, color = 'blue')
ax11.set_ylabel("Soil Moisture [ ]", fontsize = 26, fontweight = 'bold')
ax11.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax11.tick_params(axis='both', which='major', labelsize=26)
ax11.minorticks_off()
ax11.set_xticks(np.arange(1,13,1))
ax11.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])



(SrcDF.groupby(['month']).mean()['SWC_2'] / 100).plot(ax=ax12, linewidth = 2, color = 'green')
(SrgDF.groupby(['month']).mean()['SWC_1_6_1'] / 100).plot(ax=ax12, linewidth = 2, color = 'red')
(SrmDF.groupby(['month']).mean()['SWC_PI_1_7_A'] / 100).plot(ax=ax12, linewidth = 2, color = 'blue')
ax12.set_ylabel("Rootzone Moisture [ ]", fontsize = 26, fontweight = 'bold')
ax12.set_xlabel("Year", fontsize = 26, fontweight = 'bold')
ax12.tick_params(axis='both', which='major', labelsize=26)
ax12.minorticks_off()
ax12.set_xticks(np.arange(1,13,1))
ax12.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])


line_labels = ["US-Src (Creosote)", "US-Srg (Grassland)", "US-Srm (Mesquite)"]
handles, labels = ax9.get_legend_handles_labels()
fig.legend(handles, line_labels, loc='lower left', fontsize = 26)
#plt.show()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SantaRita_Monthly_Series_2.pdf", 
            bbox_inches='tight', pad_inches = 0.1,edgecolor=None)

























