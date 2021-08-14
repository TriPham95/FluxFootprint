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




# Fluxes
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Surface Energy Fluxes Time Series', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()


FmfDF['LE'].plot(ax = ax1, color = "#2ca02c", linewidth = 0.5)
ax1.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax1.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.set_ylim((-200, 700))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-200, 701, 100))
ax1.margins(y=0)
ax1.set_ylabel("Latent Heat \n Flux [W/$\mathregular{m^2}$]", fontsize = 10)
ax1.minorticks_off()


FmfDF['H'].plot(ax = ax2, color = "#2ca02c", linewidth = 0.5)
ax2.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax2.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.set_ylim((-300, 1000))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-300, 1001, 200))
ax2.margins(y=0)
ax2.set_ylabel("Sensible Heat \n Flux [W/$\mathregular{m^2}$]", fontsize = 10)
ax2.minorticks_off()


FmfDF['G'].plot(ax = ax3, color = "#2ca02c", linewidth = 0.5)
ax3.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax3.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.set_ylim((-200, 200))
ax3.yaxis.set_ticks(np.arange(-200, 201, 100))
ax3.margins(y=0)
ax3.set_ylabel("Ground Heat \n Flux [W/$\mathregular{m^2}$]", fontsize = 10)
#ax3.minorticks_off()



'''
line_labels = ["Thinning"]

fig.legend(labels = line_labels,   # The labels for each line
           loc = "center right",   # Position of legend
           borderaxespad = 0.1,    # Small spacing around legend box
           title = "Legend"  # Title for the legend
           )
'''
plt.savefig("FlagstaffComparison.png", bbox_inches='tight', pad_inches = 0)
#FufDF['TA_F'].plot(ax = ax2, color = "violet", linewidth = 0.5)




###############################################################################
# SWC, TS, NetRAD
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Net Radiation, Soil Moisture, Soil Temperature Time Series at US-Fmf', 
             fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
FmfDF['NETRAD'].plot(ax = ax1, color = "#2ca02c", linewidth = 0.5)
ax1.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax1.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax1.set_ylim((-200, 1200))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-200, 1201, 200))
ax1.margins(y=0)
ax1.set_ylabel("Net Radiation \n [W/$\mathregular{m^2}$]", fontsize = 10)
ax1.legend(['Net Radiation'], loc = 'upper left')
ax1.minorticks_off()

FmfDF['TS_1'].plot(ax = ax2, color = "#2ca02c", linewidth = 0.5)
FmfDF['TS_2'].plot(ax = ax2, color = "#ff7f0e", linewidth = 0.5)
ax2.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax2.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax2.set_ylim((-10, 40))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-10, 41, 10))
ax2.margins(y=0)
ax2.set_ylabel("Soil \n Temperature (mm)", fontsize = 10)
ax2.legend(['Surface Temp', 'Rootzone Temp'], loc = 'upper left')
ax2.minorticks_off()

(FmfDF['SWC_1']/100).plot(ax = ax3, color = "#2ca02c", linewidth = 0.5)
(FmfDF['SWC_2']/100).plot(ax = ax3, color = "#ff7f0e", linewidth = 0.5)
ax3.axvline(datetime.datetime(2005, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.axvline(datetime.datetime(2006, 9, 1), color = "black", linewidth = 1, linestyle = '--')
ax3.axvline(datetime.datetime(2007, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')
ax3.axvline(datetime.datetime(2008, 9, 1), color = "black", linewidth = 0.25, linestyle = '--')

ax3.set_ylim((0, 0.8))
ax3.yaxis.set_ticks(np.arange(0, 0.81, 0.1))
ax3.margins(y=0)
ax3.set_ylabel("Soil Moisture \n ()", fontsize = 10)
ax3.minorticks_off()
ax4 = ax3.twinx()
ax4.invert_yaxis()
FmfDF['P'].plot(ax = ax4, color = "blue", linewidth = 0.5)
ax4.set_ylim((81, 0))
ax4.margins(y=0)
ax3.legend(['SWC 10cm', 'SWC 90cm'], loc = 'upper left')

'''
line_labels = ["Thinning"]

fig.legend(labels = line_labels,   # The labels for each line
           loc = "center right",   # Position of legend
           borderaxespad = 0.1,    # Small spacing around legend box
           title = "Legend"  # Title for the legend
           )
'''
plt.savefig("/home/tpham/Windows Share/Thesis_Figures/FmfComparison_SWC.png", bbox_inches='tight', pad_inches = 0)











