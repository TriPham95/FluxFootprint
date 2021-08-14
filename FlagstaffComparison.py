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
FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200812312330]).iloc[0].name)
FmfIndexStart = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200601010000]).iloc[0].name)
FmfIndexEnd = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200812312330]).iloc[0].name)
FwfIndexStart = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200601010000]).iloc[0].name)
FwfIndexEnd = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200812312330]).iloc[0].name)


FufIndexStart = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200701010000]).iloc[0].name)
FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
FmfIndexStart = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200701010000]).iloc[0].name)
FmfIndexEnd = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
FwfIndexStart = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200701010000]).iloc[0].name)
FwfIndexEnd = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)

FufDF = FufData[FufIndexStart:FufIndexEnd]
FufDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
FwfDF = FwfData[FwfIndexStart:FwfIndexEnd]
FwfDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
FmfDF = FmfData[FmfIndexStart:FmfIndexEnd]
FmfDF.replace(to_replace = -9999, value = np.nan, inplace = True)




# Fluxes
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Surface Energy Fluxes Time Series', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()

FufDF['LE'].plot(ax = ax1, color = "#1f77b4", linewidth = 0.5)
FwfDF['LE'].plot(ax = ax1, color = "#ff7f0e", linewidth = 0.5)
FmfDF['LE'].plot(ax = ax1, color = "#2ca02c", linewidth = 0.5)
ax1.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.set_ylim((-200, 700))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-200, 701, 100))
ax1.margins(y=0)
ax1.set_ylabel("Latent Heat \n Flux (mm)", fontsize = 10)
ax1.minorticks_off()

FufDF['H'].plot(ax = ax2, color = "#1f77b4", linewidth = 0.5)
FwfDF['H'].plot(ax = ax2, color = "#ff7f0e", linewidth = 0.5)
FmfDF['H'].plot(ax = ax2, color = "#2ca02c", linewidth = 0.5)
ax2.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.set_ylim((-300, 1000))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-300, 1001, 200))
ax2.margins(y=0)
ax2.set_ylabel("Sensible Heat \n Flux (mm)", fontsize = 10)
ax2.minorticks_off()

FufDF['G_1_1_1'].plot(ax = ax3, color = "#1f77b4", linewidth = 0.5)
FwfDF['G'].plot(ax = ax3, color = "#ff7f0e", linewidth = 0.5)
FmfDF['G'].plot(ax = ax3, color = "#2ca02c", linewidth = 0.5)
ax3.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.set_ylim((-200, 200))
ax3.yaxis.set_ticks(np.arange(-200, 201, 100))
ax3.margins(y=0)
ax3.set_ylabel("Ground Heat \n Flux (mm)", fontsize = 10)
ax3.minorticks_off()

line_labels = ["Unmanaged", "Wildfire", "Thinning"]

fig.legend(labels = line_labels,   # The labels for each line
           loc = "center right",   # Position of legend
           borderaxespad = 0.1,    # Small spacing around legend box
           title = "Legend"  # Title for the legend
           )

plt.savefig("FlagstaffComparison.png", bbox_inches='tight', pad_inches = 0)
#FufDF['TA_F'].plot(ax = ax2, color = "violet", linewidth = 0.5)




###############################################################################
# SWC, TS, NetRAD
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Net Radiation, Soil Moisture, Surface Temperature Time Series', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
FwfDF['NETRAD'].plot(ax = ax1, color = "#ff7f0e", linewidth = 0.5)
FmfDF['NETRAD'].plot(ax = ax1, color = "#2ca02c", linewidth = 0.5)
FufDF['NETRAD'].plot(ax = ax1, color = "#1f77b4", linewidth = 0.5)
ax1.set_ylim((-200, 1000))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-200, 1001, 200))
ax1.margins(y=0)
ax1.set_ylabel("Net Radiation \n (mm)", fontsize = 10)
ax1.minorticks_off()

FwfDF['TS_F_MDS_1'].plot(ax = ax2, color = "#ff7f0e", linewidth = 0.5)
FmfDF['TS_F_MDS_1'].plot(ax = ax2, color = "#2ca02c", linewidth = 0.5)
FufDF['TS_F_MDS_1'].plot(ax = ax2, color = "#1f77b4", linewidth = 0.5)
ax2.set_ylim((-20, 80))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-20, 81, 10))
ax2.margins(y=0)
ax2.set_ylabel("Surface \n Temperature (mm)", fontsize = 10)
ax2.minorticks_off()

(FwfDF['SWC_F_MDS_1']/100).plot(ax = ax3, color = "#ff7f0e", linewidth = 0.5)
(FmfDF['SWC_F_MDS_1']/100).plot(ax = ax3, color = "#2ca02c", linewidth = 0.5)
(FufDF['SWC_F_MDS_1']/100).plot(ax = ax3, color = "#1f77b4", linewidth = 0.5)
ax3.set_ylim((0, 0.3))
ax3.yaxis.set_ticks(np.arange(0, 0.31, 0.1))
ax3.margins(y=0)
ax3.set_ylabel("Soil Moisture \n (mm)", fontsize = 10)
ax3.minorticks_off()


line_labels = ["Grassland", "Mesquite", "Creosote"]

fig.legend(labels = line_labels,   # The labels for each line
           loc = "center right",   # Position of legend
           borderaxespad = 0.1,    # Small spacing around legend box
           title = "Legend"  # Title for the legend
           )

plt.savefig("FlagstaffComparison_SWC.png", bbox_inches='tight', pad_inches = 0)











