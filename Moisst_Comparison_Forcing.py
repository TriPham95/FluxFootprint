#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:11:59 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

MesonetFile = '/home/tpham/Desktop/ProcessedFiles/MoisstPrecipitation.csv'
MoisstFile = '/home/tpham/Desktop/ProcessedFiles/MoisstFormatted.csv'
LAIFile = '/home/tpham/Desktop/LAI_OK.csv'
NDVIFile = '/home/tpham/Desktop/NDVI_OK.csv'
ALFile = '/home/tpham/Desktop/Albedo_OK.csv'


MoisstData = pd.read_csv(MoisstFile)
LAIData = pd.read_csv(LAIFile, header = 0)
ALData = pd.read_csv(ALFile, header = 0)
NDVIData = pd.read_csv(NDVIFile, header = 0)
MesonetData = pd.read_csv(MesonetFile)


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



MOISSTMerged = MesonetDF.merge(LAIDF_OK, left_index=True, right_index=True, how='outer')
MOISSTMerged = MOISSTMerged.merge(NDVIDF_OK, left_index=True, right_index=True, how='outer')
MOISSTMerged = MOISSTMerged.merge(ALDF_OK, left_index=True, right_index=True, how='outer')

MOISSTMerged['MOISSTLAI'] = MOISSTMerged['MOISSTLAI'].fillna(method='ffill')
MOISSTMerged['MOISSTNDVI'] = MOISSTMerged['MOISSTNDVI'].fillna(method='ffill')

Start = MOISSTMerged.index.get_loc((MOISSTMerged[MOISSTMerged.index == '2015-04-01 00:00:00']).iloc[0].name)
End = MOISSTMerged.index.get_loc((MOISSTMerged[MOISSTMerged.index == '2015-05-20 00:00:00']).iloc[0].name)

MOISSTMerged = MOISSTMerged[Start:(End+1)]


###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, (ax1, ax7, ax8, ax9, ax2,ax3,ax4,ax5,ax6) = plt.subplots(9, 1, figsize=(20,28))
fig.subplots_adjust(top=0.95)

ax1.invert_yaxis()
MOISSTMerged['P_sum'].plot.bar(ax = ax1, label = "Precipitation", color = 'black')
ax1.axvline(MOISSTMerged.index.searchsorted('2015-04-20'), color = "C1", linewidth = 1)
ax1.set_ylim((51, 0))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0,51, 20))
ax1.margins(y=0)
ax1.set_ylabel("P [mm]", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.get_xaxis().set_visible(False)

MOISSTMerged['MOISSTLAI'].plot(ax = ax7, label = "LAI", linewidth = 2, color = 'black')
ax7.set_xticklabels([])
ax7.xaxis.label.set_visible(False)
#ax2.margins(y=0)
ax7.set_ylabel("LAI []", fontsize = 22, fontweight = 'bold')
ax7.minorticks_off()
ax7.get_xaxis().set_visible(False)
#ax2.legend()
ax7.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)

MOISSTMerged['MOISSTAL'].plot(ax = ax8, label = "Albedo", linewidth = 2, color = 'black')
ax8.set_xticklabels([])
ax8.xaxis.label.set_visible(False)
#ax2.margins(y=0)
ax8.set_ylabel("Albedo []", fontsize = 22, fontweight = 'bold')
ax8.minorticks_off()
ax8.get_xaxis().set_visible(False)
#ax2.legend()
ax8.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)


MOISSTMerged['MOISSTNDVI'].plot(ax = ax9, label = "NDVI", linewidth = 2, color = 'black')
ax9.set_xticklabels([])
ax9.xaxis.label.set_visible(False)
#ax2.margins(y=0)
ax9.set_ylabel("NDVI []", fontsize = 22, fontweight = 'bold')
ax9.minorticks_off()
ax9.get_xaxis().set_visible(False)
#ax2.legend()
ax9.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)

MOISSTMerged['SRAD'].plot(ax = ax2, label = "Shortwave Radiation", linewidth = 2, color = 'black')
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
#ax2.margins(y=0)
ax2.set_ylabel("SW [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax2.minorticks_off()
ax2.get_xaxis().set_visible(False)
#ax2.legend()
ax2.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax2.set_ylim((-20, 41))
#ax2.yaxis.set_ticks(np.arange(-20, 41, 20))
#ax2.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

MOISSTMerged['TAIR'].plot(ax = ax3, label = "Air Temperature", linewidth = 2, color = 'black')
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.margins(y=0)
ax3.set_ylabel("TA [\xb0C]", fontsize = 22, fontweight = 'bold')
ax3.minorticks_off()
ax3.get_xaxis().set_visible(False)
#ax3.legend()
ax3.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax3.set_ylim((0, 1000))
#ax3.yaxis.set_ticks(np.arange(0, 1201, 200))
#ax3.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

(MOISSTMerged['WSPD']*100).plot(ax = ax4, label = "Wind Speed", linewidth = 2, color = 'black')
ax4.set_xticklabels([])
ax4.xaxis.label.set_visible(False)
ax4.margins(y=0)
ax4.set_ylabel("WS [m/s]", fontsize = 22, fontweight = 'bold')
ax4.minorticks_off()
ax4.get_xaxis().set_visible(False)
#ax4.legend()
ax4.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax4.set_ylim((0, 101))
#ax4.yaxis.set_ticks(np.arange(0, 101, 20))
#ax4.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

(MOISSTMerged['PRES']*33.8639).plot(ax = ax5, label = "Air Pressure", linewidth = 2, color = 'black')
ax5.set_xticklabels([])
ax5.xaxis.label.set_visible(False)
ax5.margins(y=0)
ax5.set_ylabel("PA [mbar]", fontsize = 22, fontweight = 'bold')
ax5.minorticks_off()
ax5.get_xaxis().set_visible(False)
ax5.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax5.set_ylim((0, 15.1))
#ax5.yaxis.set_ticks(np.arange(0, 15.1, 5))
#ax5.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')
#ax5.legend()

(MOISSTMerged['RELH']*100).plot(ax = ax6, label = "Relative Humidity", linewidth = 2, color = 'black')
#ax6.set_xticklabels([])
#ax6.xaxis.label.set_visible(False)
ax6.margins(y=0)
ax6.set_ylabel("RH [%]", fontsize = 22, fontweight = 'bold')
#ax6.set_ylim((28, 30))
#ax6.yaxis.set_ticks(np.arange(28, 31, 1))
#ax6.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')
ax6.set_xlabel("Date", fontsize = 22, fontweight = 'bold')
ax6.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax6.minorticks_off()
#ax5.set_xticklabels([])
#ax6.legend()
ax6.xaxis.set_major_locator(mdates.MonthLocator())
ax6.xaxis.set_major_formatter(mdates.DateFormatter('\n %b'))

#ax6.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
#ax6.xaxis.set_minor_locator(mdates.DayLocator(interval = 5))



plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Moisst_Comparison_HydroMetr2015_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)





























