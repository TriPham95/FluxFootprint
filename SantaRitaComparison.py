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



SrcFile = '/home/tpham/Desktop/USSrc.csv'
SrmFile = '/home/tpham/Desktop/USSrm.csv'
SrgFile = '/home/tpham/Desktop/USSrg.csv'


SrcData = pd.read_csv(SrcFile)
SrmData = pd.read_csv(SrmFile)
SrgData = pd.read_csv(SrgFile)

SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcData['TIMESTAMP_START']])
SrcData.set_index('Time', inplace = True, drop = True)

SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData.set_index('Time', inplace = True, drop = True)

SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData.set_index('Time', inplace = True, drop = True)



SrcIndexStart = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
SrcIndexEnd = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)
SrmIndexStart = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
SrmIndexEnd = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)
SrgIndexStart = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
SrgIndexEnd = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)

SrcDF = SrcData[SrcIndexStart:SrcIndexEnd]
SrcDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrgDF = SrgData[SrgIndexStart:SrgIndexEnd]
SrgDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrmDF = SrmData[SrmIndexStart:SrmIndexEnd]
SrmDF.replace(to_replace = -9999, value = np.nan, inplace = True)




# Fluxes
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Surface Energy Fluxes Time Series', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
SrgDF['LE_F_MDS'].plot(ax = ax1, color = "#ff7f0e", linewidth = 0.5)
SrmDF['LE_F_MDS'].plot(ax = ax1, color = "#2ca02c", linewidth = 0.5)
SrcDF['LE_F_MDS'].plot(ax = ax1, color = "#1f77b4", linewidth = 0.5)
ax1.set_ylim((-100, 600))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-100, 601, 100))
ax1.margins(y=0)
ax1.set_ylabel("Latent Heat \n Flux (mm)", fontsize = 10)
ax1.minorticks_off()

SrgDF['H_F_MDS'].plot(ax = ax2, color = "#ff7f0e", linewidth = 0.5)
SrmDF['H_F_MDS'].plot(ax = ax2, color = "#2ca02c", linewidth = 0.5)
SrcDF['H_F_MDS'].plot(ax = ax2, color = "#1f77b4", linewidth = 0.5)
ax2.set_ylim((-200, 600))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-200, 601, 100))
ax2.margins(y=0)
ax2.set_ylabel("Sensible Heat \n Flux (mm)", fontsize = 10)
ax2.minorticks_off()

SrgDF['G_F_MDS'].plot(ax = ax3, color = "#ff7f0e", linewidth = 0.5)
SrmDF['G_F_MDS'].plot(ax = ax3, color = "#2ca02c", linewidth = 0.5)
SrcDF['G_F_MDS'].plot(ax = ax3, color = "#1f77b4", linewidth = 0.5)

ax3.set_ylim((-300, 400))
ax3.yaxis.set_ticks(np.arange(-200, 401, 100))
ax3.margins(y=0)
ax3.set_ylabel("Ground Heat \n Flux (mm)", fontsize = 10)
ax3.minorticks_off()

line_labels = ["Grassland", "Mesquite", "Creosote"]

fig.legend(labels = line_labels,   # The labels for each line
           loc = "center right",   # Position of legend
           borderaxespad = 0.1,    # Small spacing around legend box
           title = "Legend"  # Title for the legend
           )

plt.savefig("SantaRitaComparison.png", bbox_inches='tight', pad_inches = 0)
#SrcDF['TA_F'].plot(ax = ax2, color = "violet", linewidth = 0.5)




###############################################################################
# SWC, TS, NetRAD
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Net Radiation, Soil Moisture, Surface Temperature Time Series', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
SrgDF['NETRAD'].plot(ax = ax1, color = "#ff7f0e", linewidth = 0.5)
SrmDF['NETRAD'].plot(ax = ax1, color = "#2ca02c", linewidth = 0.5)
SrcDF['NETRAD'].plot(ax = ax1, color = "#1f77b4", linewidth = 0.5)
ax1.set_ylim((-200, 1000))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-200, 1001, 200))
ax1.margins(y=0)
ax1.set_ylabel("Net Radiation \n (mm)", fontsize = 10)
ax1.minorticks_off()

SrgDF['TS_F_MDS_1'].plot(ax = ax2, color = "#ff7f0e", linewidth = 0.5)
SrmDF['TS_F_MDS_1'].plot(ax = ax2, color = "#2ca02c", linewidth = 0.5)
SrcDF['TS_F_MDS_1'].plot(ax = ax2, color = "#1f77b4", linewidth = 0.5)
ax2.set_ylim((-20, 80))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-20, 81, 10))
ax2.margins(y=0)
ax2.set_ylabel("Surface \n Temperature (mm)", fontsize = 10)
ax2.minorticks_off()

(SrgDF['SWC_F_MDS_1']/100).plot(ax = ax3, color = "#ff7f0e", linewidth = 0.5)
(SrmDF['SWC_F_MDS_1']/100).plot(ax = ax3, color = "#2ca02c", linewidth = 0.5)
(SrcDF['SWC_F_MDS_1']/100).plot(ax = ax3, color = "#1f77b4", linewidth = 0.5)
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

plt.savefig("SantaRitaComparison_SWC.png", bbox_inches='tight', pad_inches = 0)











