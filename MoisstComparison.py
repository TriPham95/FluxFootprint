#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:09:33 2019

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec


MoisstFile = '/home/tpham/Desktop/ProcessedFiles/MoisstFormatted.csv'
LAIFile = '/home/tpham/Desktop/LAI_OK.csv'
NDVIFile = '/home/tpham/Desktop/NDVI_OK.csv'
ALFile = '/home/tpham/Desktop/Albedo_OK.csv'


MoisstData = pd.read_csv(MoisstFile)
LAIData = pd.read_csv(LAIFile, header = 0)
ALData = pd.read_csv(ALFile, header = 0)
NDVIData = pd.read_csv(NDVIFile, header = 0)

###############################################################################
LAIData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in LAIData['Date ']])

LAIData.set_index('Time', inplace = True, drop = True)
LAIData.replace(to_replace = 'NA', value = np.nan, inplace = True) 
#LAIData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
#                        for x in LAIData['Date ']])
#LAIData['month'] = ([datetime.datetime.strftime(x, '%m') 
#                        for x in LAIData['month']])
#LAIData['month'].astype(float)
#LAIDF = LAIData.apply(pd.to_numeric).resample("M").mean()
#LAIDF['month'] = LAIDF['month'].astype(int)

Start = LAIData.index.get_loc((LAIData[LAIData.index == '2014-01-01']).iloc[0].name)
End = LAIData.index.get_loc((LAIData[LAIData.index == '2015-12-31']).iloc[0].name)
LAIDF_OK = LAIData[Start:End]

###############################################################################
NDVIData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in NDVIData['Date']])

NDVIData.set_index('Time', inplace = True, drop = True)
NDVIData.replace(to_replace = 'NA', value = np.nan, inplace = True) 
#NDVIData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
#                        for x in NDVIData['Date']])
#NDVIData['month'] = ([datetime.datetime.strftime(x, '%m') 
#                        for x in NDVIData['month']])
#NDVIData['month'].astype(float)
#NDVIDF = NDVIData.apply(pd.to_numeric).resample("M").mean()
#NDVIDF['month'] = NDVIDF['month'].astype(int)

Start = NDVIData.index.get_loc((NDVIData[NDVIData.index == '2014-01-01']).iloc[0].name)
End = NDVIData.index.get_loc((NDVIData[NDVIData.index == '2015-12-31']).iloc[0].name)
NDVIDF_OK = NDVIData[Start:End]

###############################################################################
ALData.replace(to_replace = 'NA ', value = np.nan, inplace = True) 
ALData.dropna(inplace = True)

ALData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in ALData['Date ']])

ALData.set_index('Time', inplace = True, drop = True)

#ALData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
#                       for x in ALData['Date ']])
#ALData['month'] = ([datetime.datetime.strftime(x, '%m') 
#                        for x in ALData['month']])
#ALData['month'].astype(float)
#ALDF = ALData.apply(pd.to_numeric).resample("M").mean()

#ALDF['month'] = ALDF['month'].astype(int)

Start = ALData.index.get_loc((ALData[ALData.index == '2014-01-01']).iloc[0].name)
End = ALData.index.get_loc((ALData[ALData.index == '2015-12-31']).iloc[0].name)
ALDF_OK = ALData[Start:End]


###############################################################################
MoisstData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in MoisstData['Timestamp']])
MoisstData.set_index('Time', inplace = True, drop = True)

#MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201504010000]).iloc[0].name)
#MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201505200000]).iloc[0].name)

MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201401010000]).iloc[0].name)
MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201512310000]).iloc[0].name)

MoisstDF = MoisstData[MoisstIndexStart:MoisstIndexEnd]
MoisstDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstDF['Day'] = ([datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') 
                       for x in MoisstDF.index])
MoisstDF['Day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in MoisstDF['Day']])

MoisstDF = MoisstDF.apply(pd.to_numeric).resample("D").mean()

###############################################################################
MesonetFile = '/home/tpham/Desktop/ProcessedFiles/MoisstPrecipitation.csv'

MesonetData = pd.read_csv(MesonetFile)
MesonetData.replace(-999, float('nan'), inplace=True)

MesonetData['Time'] = ([datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M') 
                        for x in MesonetData['TIME']])
MesonetData['TAIR'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TAIR']])
MesonetData['TDEW'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TDEW']])
MesonetData['RELH'] = (["{0:.2f}".format(float(x) / 100) 
                        for x in MesonetData['RELH']])
MesonetData['RAIN'] = (["{0:.4f}".format(float(x) * 25.4) 
                        for x in MesonetData['RAIN']])
MesonetData['PRES'] = (["{0:.4f}".format(float(x) * 1) 
                        for x in MesonetData['PRES']])
MesonetData['SRAD'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['SRAD']])
MesonetData['WSPD'] = (["{0:.2f}".format(float(x) * 0.44704) 
                        for x in MesonetData['WSPD']])
MesonetData['WDIR'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['WDIR']])
MesonetData.drop(['STID', 'TIME', 'TMIN', 'TMAX', 'WMAX'], axis = 1, inplace = True)
MesonetData.set_index('Time', inplace = True, drop = True)
MesonetData = MesonetData.astype('float32')
Start = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2014-01-01 00:00:00']).iloc[0].name)
End = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-12-31 23:00:00']).iloc[0].name)
MesonetData = MesonetData[Start:(End+1)]

MesonetData['Day'] = ([datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') 
                       for x in MesonetData.index])
MesonetData['Day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in MesonetData['Day']])

MesonetDF = MesonetData.apply(pd.to_numeric).resample("D").mean()
MesonetDF['P_sum'] = MesonetData['RAIN'].apply(pd.to_numeric).resample("D").sum()


###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
#fig, ((ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10)) = plt.subplots(10, 1, figsize=(20,36))

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


LAIDF_OK['MOISSTLAI'].plot(ax=ax1, linewidth = 2, color = 'black')
ax1.set_ylabel("LAI [ ]", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.tick_params(axis='both', which='major', labelsize=22)
ax1.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax1.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.set_xticklabels([])
ax1.get_xaxis().set_visible(False)

ALDF_OK['MOISSTAL'].plot(ax=ax2, linewidth = 2, color = 'black')
ax2.set_ylabel("Albedo [ ]", fontsize = 22, fontweight = 'bold')
ax2.minorticks_off()
ax2.tick_params(axis='both', which='major', labelsize=22)
ax2.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax2.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.get_xaxis().set_visible(False)


NDVIDF_OK['MOISSTNDVI'].plot(ax=ax3, linewidth = 2, color = 'black')
ax3.set_ylabel("NDVI [ ]", fontsize = 22, fontweight = 'bold')
ax3.minorticks_off()
ax3.tick_params(axis='both', which='major', labelsize=22)
ax3.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax3.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax3.minorticks_off()
ax3.set_xticklabels([])
ax3.get_xaxis().set_visible(False)

MoisstDF['Rn_total_Avg'].plot(ax = ax4, linewidth = 2, color = 'black')
ax4.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax4.set_ylim((-100, 300))
ax4.yaxis.set_ticks(np.arange(-100, 301, 100))
ax4.margins(y=0)
ax4.set_ylabel("NETRAD [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax4.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax4.minorticks_off()
ax4.set_xticklabels([])
ax4.get_xaxis().set_visible(False)

MoisstDF['LE_wpl'].plot(ax = ax5, linewidth = 2, color = 'black')
ax5.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax5.set_ylim((0, 200))
ax5.yaxis.set_ticks(np.arange(0, 201, 50))
ax5.margins(y=0)
ax5.set_ylabel("Latent Heat Flux [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax5.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax5.minorticks_off()
ax5.set_xticklabels([])
ax5.get_xaxis().set_visible(False)

MoisstDF['Hs'].plot(ax = ax6, linewidth = 2, color = 'black')
ax6.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax6.set_ylim((-50, 150))
ax6.yaxis.set_ticks(np.arange(-50, 151, 50))
ax6.margins(y=0)
ax6.set_ylabel("Sensible Heat Flux [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax6.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax6.minorticks_off()
ax6.set_xticklabels([])
ax6.get_xaxis().set_visible(False)

MoisstDF['SHF1_Avg'].plot(ax = ax7, linewidth = 2, color = 'black')
ax7.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax7.set_ylim((-20, 20))
ax7.yaxis.set_ticks(np.arange(-20, 21, 10))
ax7.margins(y=0)
ax7.set_ylabel("Ground Heat Flux [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax7.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax7.minorticks_off()
ax7.set_xticklabels([])
ax7.xaxis.set_major_locator(mdates.MonthLocator(interval = 3))
ax7.xaxis.set_major_formatter(mdates.DateFormatter('%b'))


MoisstDF['SoilTC1_Avg'].plot(ax = ax8, linewidth = 2, color = 'black')
ax8.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax8.set_ylim((0, 40))
ax8.yaxis.set_ticks(np.arange(0, 41, 20))
ax8.margins(y=0)
ax8.set_ylabel("Surface Temperature [\xb0C]", fontsize = 22, fontweight = 'bold')
ax8.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax8.minorticks_off()
ax8.set_xticklabels([])
ax8.get_xaxis().set_visible(False)


MoisstDF['SWC5'].plot(ax = ax9, linewidth = 2, color = 'black')
ax9.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax9.set_ylim((0, 0.6))
ax9.yaxis.set_ticks(np.arange(0, 0.61, 0.2))
ax9.margins(y=0)
ax9.set_ylabel("Surface Soil Moisture [ ]", fontsize = 22, fontweight = 'bold')
ax9.set_xlabel("", fontsize = 22, fontweight = 'bold')
ax9.minorticks_off()
ax9.set_xticklabels([])
ax9.xaxis.set_major_locator(mdates.MonthLocator(interval = 3))
ax9.xaxis.set_major_formatter(mdates.DateFormatter('%b'))


ax10.set_ylim((0, 91))
ax10.yaxis.set_ticks(np.arange(0, 91, 20))
MesonetDF['P_sum'].plot(ax=ax10, linewidth = 2, color = 'black')
ax10.set_ylabel("P [mm]", fontsize = 22, fontweight = 'bold')
ax10.minorticks_off()
ax10.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax10.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax10.minorticks_off()
ax10.set_xticklabels([])
ax10.xaxis.set_major_locator(mdates.MonthLocator(interval = 3))
ax10.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax10.xaxis.set_tick_params(rotation=0)




plt.savefig("/home/tpham/Windows Share/Thesis_Figures/MOISST_TwoYear_Comparison.svg", 
            bbox_inches='tight', pad_inches = 0.1)































'''
###############################################################################
# Fluxes
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(20, 12))
fig.subplots_adjust(top = 0.95)
fig.suptitle('Surface Energy Fluxes Time Series in April and May 2015 at Northeast Patch', 
             fontsize = 14, fontweight = 'bold')
plt.minorticks_off()
MoisstDF['Rn_total_Avg'].plot(ax = ax1, linewidth = 2)
ax1.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax1.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax1.set_ylim((-100, 1000))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-100, 1001, 200))
ax1.margins(y=0)
ax1.set_ylabel("NETRAD [W/$\mathregular{m^2}$]", fontsize = 14, fontweight = 'bold')
#ax1.minorticks_off()

MoisstDF['LE_wpl'].plot(ax = ax2, linewidth = 2)
ax2.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax2.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax2.set_ylim((-100, 400))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-100, 401, 100))
ax2.margins(y=0)
ax2.set_ylabel("LE [W/$\mathregular{m^2}$]", fontsize = 14, fontweight = 'bold')
#ax2.minorticks_off()

MoisstDF['Hs'].plot(ax = ax3, linewidth = 2)
ax3.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax3.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax3.set_ylim((-200, 400))
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.yaxis.set_ticks(np.arange(-200, 401, 100))
ax3.margins(y=0)
ax3.set_ylabel("H [W/$\mathregular{m^2}$]", fontsize = 14, fontweight = 'bold')
#ax3.minorticks_off()

MoisstDF['SHF1_Avg'].plot(ax = ax4, linewidth = 2)
ax4.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax4.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax4.set_ylim((-100, 100))
ax4.yaxis.set_ticks(np.arange(-100, 101, 50))
ax4.margins(y=0)
ax4.set_ylabel("G [W/$\mathregular{m^2}$]", fontsize = 14, fontweight = 'bold')
ax4.set_xlabel("Time", fontsize = 14, fontweight = 'bold')
#ax4.minorticks_off()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Moisst_April2015.png", 
            bbox_inches='tight', pad_inches = 0.1)




###############################################################################
# SWC
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(20, 12))
fig.subplots_adjust(top = 0.95)
#fig.suptitle('Surface Energy Fluxes Time Series in April and May 2015 at Northeast Patch', 
#             fontsize = 14, fontweight = 'bold')
plt.minorticks_off()
MoisstDF['SWC10'].plot(ax = ax1, linewidth = 2)
ax1.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax1.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax1.set_ylim((0, 0.8))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 0.81, 0.2))
ax1.margins(y=0)
ax1.set_ylabel("SWC10 [ ]", fontsize = 14, fontweight = 'bold')
#ax1.minorticks_off()

MoisstDF['SWC90'].plot(ax = ax2, linewidth = 2)
ax2.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax2.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax2.set_ylim((0.2, 0.6))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(0.2, 0.61, 0.2))
ax2.margins(y=0)
ax2.set_ylabel("SWC90 [ ]", fontsize = 14, fontweight = 'bold')
#ax2.minorticks_off()

MoisstDF['SoilTC3_Avg'].plot(ax = ax3, linewidth = 2)
ax3.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax3.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax3.set_ylim((10, 30))
ax3.yaxis.set_ticks(np.arange(10, 31, 10))
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.margins(y=0)
ax3.set_ylabel(" Troot [\xb0C]", fontsize = 14, fontweight = 'bold')
#ax4.minorticks_off()


MoisstDF['SoilTC5_Avg'].plot(ax = ax4, linewidth = 2)
ax4.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax4.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax4.set_ylim((10, 30))
ax4.yaxis.set_ticks(np.arange(10, 31, 10))
ax4.margins(y=0)
ax4.set_ylabel(" Troot [\xb0C]", fontsize = 14, fontweight = 'bold')
ax4.set_xlabel("Time", fontsize = 14, fontweight = 'bold')
#ax4.minorticks_off()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Moisst_SWC_April2015.png", 
            bbox_inches='tight', pad_inches = 0.1)










###############################################################################
MesonetFile = '/home/tpham/Desktop/MoisstPrecipitation.csv'

MesonetData = pd.read_csv(MesonetFile)
MesonetData.replace(-999, float('nan'), inplace=True)

MesonetData['Time'] = ([datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M') 
                        for x in MesonetData['TIME']])
MesonetData['TAIR'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TAIR']])
MesonetData['TDEW'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TDEW']])
MesonetData['RELH'] = (["{0:.2f}".format(float(x) / 100) 
                        for x in MesonetData['RELH']])
MesonetData['RAIN'] = (["{0:.4f}".format(float(x) * 25.4) 
                        for x in MesonetData['RAIN']])
MesonetData['PRES'] = (["{0:.4f}".format(float(x) * 1) 
                        for x in MesonetData['PRES']])
MesonetData['SRAD'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['SRAD']])
MesonetData['WSPD'] = (["{0:.2f}".format(float(x) * 0.44704) 
                        for x in MesonetData['WSPD']])
MesonetData['WDIR'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['WDIR']])
MesonetData.drop(['STID', 'TIME', 'TMIN', 'TMAX', 'WMAX'], axis = 1, inplace = True)
MesonetData.set_index('Time', inplace = True, drop = True)
MesonetData = MesonetData.astype('float32')
Start = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-04-01 00:00:00']).iloc[0].name)
End = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-05-20 00:00:00']).iloc[0].name)
MesonetData = MesonetData[Start:End]



fig, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(6, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)

ax1.invert_yaxis()
MesonetData['RAIN'].plot(ax = ax1, kind='bar', label = "Precipitation")
ax1.set_ylim((41, 0))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0,41, 10))
ax1.margins(y=0)
ax1.set_ylabel("P [mm]", fontsize = 14, fontweight = 'bold')
#ax1.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')
ax1.minorticks_off()
ax1.get_xaxis().set_visible(False)
ax1.legend()
ax1.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)

MesonetData['SRAD'].plot(ax = ax2, label = "Shortwave Radiation")
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
#ax2.margins(y=0)
ax2.set_ylabel("SW [W/$\mathregular{m^2}$]", fontsize = 14, fontweight = 'bold')
ax2.minorticks_off()
ax2.get_xaxis().set_visible(False)
ax2.legend()
ax2.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax2.set_ylim((-20, 41))
#ax2.yaxis.set_ticks(np.arange(-20, 41, 20))
#ax2.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

MesonetData['TAIR'].plot(ax = ax3, label = "Air Temperature")
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.margins(y=0)
ax3.set_ylabel("TA [\xb0C]", fontsize = 14, fontweight = 'bold')
ax3.minorticks_off()
ax3.get_xaxis().set_visible(False)
ax3.legend()
ax3.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax3.set_ylim((0, 1000))
#ax3.yaxis.set_ticks(np.arange(0, 1201, 200))
#ax3.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

(MesonetData['WSPD']*100).plot(ax = ax4, label = "Wind Speed")
ax4.set_xticklabels([])
ax4.xaxis.label.set_visible(False)
ax4.margins(y=0)
ax4.set_ylabel("WS [m/s]", fontsize = 14, fontweight = 'bold')
ax4.minorticks_off()
ax4.get_xaxis().set_visible(False)
ax4.legend()
ax4.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax4.set_ylim((0, 101))
#ax4.yaxis.set_ticks(np.arange(0, 101, 20))
#ax4.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

(MesonetData['PRES']*33.8639).plot(ax = ax5, label = "Air Pressure")
ax5.set_xticklabels([])
ax5.xaxis.label.set_visible(False)
ax5.margins(y=0)
ax5.set_ylabel("PA [mbar]", fontsize = 14, fontweight = 'bold')
ax5.minorticks_off()
ax5.get_xaxis().set_visible(False)
ax5.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax5.set_ylim((0, 15.1))
#ax5.yaxis.set_ticks(np.arange(0, 15.1, 5))
#ax5.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')
ax5.legend()

(MesonetData['RELH']*100).plot(ax = ax6, label = "Relative Humidity")
#ax6.set_xticklabels([])
#ax6.xaxis.label.set_visible(False)
ax6.margins(y=0)
ax6.set_ylabel("RH [%]", fontsize = 14, fontweight = 'bold')
#ax6.set_ylim((28, 30))
#ax6.yaxis.set_ticks(np.arange(28, 31, 1))
#ax6.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')
ax6.set_xlabel("Month", fontsize = 14, fontweight = 'bold')
ax6.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax6.minorticks_off()
#ax5.set_xticklabels([])
ax6.legend()




plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Moisst_HydroMetr2015.png", 
            bbox_inches='tight', pad_inches = 0.1)


###############################################################################
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Net Radiation, Soil Moisture, Surface Temperature Time Series', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
MoisstDF['SWC10'].plot(ax = ax1, color = "#1f77b4", linewidth = 1)
ax1.axvline(datetime.datetime(2015, 4, 15), color = "#d62728", linewidth = 0.25)
#ax1.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax1.set_ylim((0, 0.5))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 0.51, 0.1))
ax1.margins(y=0)
ax1.set_ylabel("Soil Moisture \n (mm)", fontsize = 10)
#ax1.minorticks_off()


MoisstDF['SWC90'].plot(ax = ax1, color = "#1f77b4", linewidth = 1)
ax2.axvline(datetime.datetime(2015, 4, 15), color = "#d62728", linewidth = 0.25)
#ax1.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax2.set_ylim((0, 0.5))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(0, 0.51, 0.1))
ax2.margins(y=0)
ax2.set_ylabel("Soil Moisture \n (mm)", fontsize = 10)
#ax2.minorticks_off()

MoisstDF['SHF1_Avg'].plot(ax = ax3, color = "#1f77b4", linewidth = 1)
ax3.axvline(datetime.datetime(2015, 4, 15), color = "#d62728", linewidth = 0.25)
#ax3.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax3.set_ylim((-100, 100))
ax3.yaxis.set_ticks(np.arange(-100, 101, 50))
ax3.margins(y=0)
ax3.set_ylabel("Ground Heat \n Flux (mm)", fontsize = 10)
#ax3.minorticks_off()


'''





