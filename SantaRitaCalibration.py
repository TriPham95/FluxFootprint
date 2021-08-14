#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:30:19 2019

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



SrcIndexStart = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrcIndexEnd = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 201001010030]).iloc[0].name)

SrmIndexStart = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrmIndexEnd = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 201001010030]).iloc[0].name)

SrgIndexStart = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
SrgIndexEnd = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 201001010030]).iloc[0].name)





SrcDF = SrcData[SrcIndexStart:SrcIndexEnd]
SrcDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrgDF = SrgData[SrgIndexStart:SrgIndexEnd]
SrgDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrmDF = SrmData[SrmIndexStart:SrmIndexEnd]
SrmDF.replace(to_replace = -9999, value = np.nan, inplace = True)



###############################################################################
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Forcing Parameters for US-Src', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
ax1.invert_yaxis()
SrcDF['P_F'].plot(ax = ax1, color = "blue", linewidth = 1.5)
ax1.set_ylim((30, 0))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 31, 10))
ax1.margins(y=0)
ax1.set_ylabel("Precipitation \n (mm)", fontsize = 10)
ax1.minorticks_off()
SrcDF['TA_F'].plot(ax = ax2, color = "violet", linewidth = 0.5)
#SrmDF['TA_F'].plot(ax = ax1, color = "green", linewidth = 0.5)
#SrgDF['TA_F'].plot(ax = ax1, color = "darkblue", linewidth = 0.5)
ax2.set_ylim((-10, 50))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-10, 51, 10))
ax2.margins(y=0)
ax2.set_ylabel("Air \n Temperature \n (C)", fontsize = 10)
ax2.minorticks_off()
SrcDF['SW_IN_F'].plot(ax = ax3, color = "red", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax3.set_ylim((0, 1200))
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.yaxis.set_ticks(np.arange(0, 1201, 200))
ax3.margins(y=0)
ax3.set_ylabel("Shortwave \n Radiation \n (W.m-2)", fontsize = 10)
ax3.minorticks_off()
(SrcDF['PA_F']*10).plot(ax = ax4, color = "orange", linewidth = 0.5)
ax4.set_ylim((880, 920))
ax4.set_xticklabels([])
ax4.xaxis.label.set_visible(False)
ax4.yaxis.set_ticks(np.arange(880, 921, 10))
ax4.margins(y=0)
ax4.set_ylabel("Air \n Pressure \n (mbar)", fontsize = 10)
ax4.minorticks_off()
SrcDF['RH'].plot(ax = ax5, color = "brown", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax5.set_ylim((0, 110))
ax5.set_xticklabels([])
ax5.xaxis.label.set_visible(False)
ax5.yaxis.set_ticks(np.arange(0, 111, 20))
ax5.margins(y=0)
ax5.set_ylabel("Relative \n Humidity \n (%)", fontsize = 10)
ax5.minorticks_off()
SrcDF['WS_F'].plot(ax = ax6, color = "green", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax6.set_ylim((0, 10))
ax6.yaxis.set_ticks(np.arange(0, 11, 2))
ax6.margins(y=0)
ax6.set_ylabel("Wind Speed \n (m/s)", fontsize = 10)
ax6.minorticks_off()
plt.savefig("test.png", bbox_inches='tight', pad_inches = 0)
###############################################################################
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Forcing Parameters for US-Srm', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
ax1.invert_yaxis()
SrmDF['P_F'].plot(ax = ax1, color = "blue", linewidth = 1.5)
ax1.set_ylim((30, 0))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 31, 10))
ax1.margins(y=0)
ax1.set_ylabel("Precipitation \n (mm)", fontsize = 10)
ax1.minorticks_off()
SrmDF['TA_F'].plot(ax = ax2, color = "violet", linewidth = 0.5)
#SrmDF['TA_F'].plot(ax = ax1, color = "green", linewidth = 0.5)
#SrgDF['TA_F'].plot(ax = ax1, color = "darkblue", linewidth = 0.5)
ax2.set_ylim((-10, 50))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-10, 51, 10))
ax2.margins(y=0)
ax2.set_ylabel("Air \n Temperature \n (C)", fontsize = 10)
ax2.minorticks_off()
SrmDF['SW_IN_F'].plot(ax = ax3, color = "red", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax3.set_ylim((0, 1200))
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.yaxis.set_ticks(np.arange(0, 1201, 200))
ax3.margins(y=0)
ax3.set_ylabel("Shortwave \n Radiation \n (W.m-2)", fontsize = 10)
ax3.minorticks_off()
(SrmDF['PA_F']*10).plot(ax = ax4, color = "orange", linewidth = 0.5)
ax4.set_ylim((880, 900))
ax4.set_xticklabels([])
ax4.xaxis.label.set_visible(False)
ax4.yaxis.set_ticks(np.arange(880, 901, 10))
ax4.margins(y=0)
ax4.set_ylabel("Air \n Pressure \n (mbar)", fontsize = 10)
ax4.minorticks_off()
SrmDF['RH'].plot(ax = ax5, color = "brown", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax5.set_ylim((0, 110))
ax5.set_xticklabels([])
ax5.xaxis.label.set_visible(False)
ax5.yaxis.set_ticks(np.arange(0, 111, 20))
ax5.margins(y=0)
ax5.set_ylabel("Relative \n Humidity \n (%)", fontsize = 10)
ax5.minorticks_off()
SrmDF['WS_F'].plot(ax = ax6, color = "green", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax6.set_ylim((0, 10))
ax6.yaxis.set_ticks(np.arange(0, 11, 2))
ax6.margins(y=0)
ax6.set_ylabel("Wind Speed \n (m/s)", fontsize = 10)
ax6.minorticks_off()
plt.savefig("SrmForcing.png", bbox_inches='tight', pad_inches = 0)


###############################################################################
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, figsize=(15, 8))
fig.subplots_adjust(top=0.95)
fig.suptitle('Forcing Parameters for US-Srg', fontsize = 12, fontweight = 'bold')
plt.minorticks_off()
ax1.invert_yaxis()
SrgDF['P_F'].plot(ax = ax1, color = "blue", linewidth = 1.5)
ax1.set_ylim((30, 0))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(0, 31, 10))
ax1.margins(y=0)
ax1.set_ylabel("Precipitation \n (mm)", fontsize = 10)
ax1.minorticks_off()
SrgDF['TA_F'].plot(ax = ax2, color = "violet", linewidth = 0.5)
#SrmDF['TA_F'].plot(ax = ax1, color = "green", linewidth = 0.5)
#SrgDF['TA_F'].plot(ax = ax1, color = "darkblue", linewidth = 0.5)
ax2.set_ylim((-10, 50))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-10, 51, 10))
ax2.margins(y=0)
ax2.set_ylabel("Air \n Temperature \n (C)", fontsize = 10)
ax2.minorticks_off()
SrgDF['SW_IN_F'].plot(ax = ax3, color = "red", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax3.set_ylim((0, 1200))
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.yaxis.set_ticks(np.arange(0, 1201, 200))
ax3.margins(y=0)
ax3.set_ylabel("Shortwave \n Radiation \n (W.m-2)", fontsize = 10)
ax3.minorticks_off()
(SrgDF['PA_F']*10).plot(ax = ax4, color = "orange", linewidth = 0.5)
ax4.set_ylim((850, 890))
ax4.set_xticklabels([])
ax4.xaxis.label.set_visible(False)
ax4.yaxis.set_ticks(np.arange(850, 891, 10))
ax4.margins(y=0)
ax4.set_ylabel("Air \n Pressure \n (mbar)", fontsize = 10)
ax4.minorticks_off()
SrgDF['RH'].plot(ax = ax5, color = "brown", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax5.set_ylim((0, 110))
ax5.set_xticklabels([])
ax5.xaxis.label.set_visible(False)
ax5.yaxis.set_ticks(np.arange(0, 111, 20))
ax5.margins(y=0)
ax5.set_ylabel("Relative \n Humidity \n (%)", fontsize = 10)
ax5.minorticks_off()
SrgDF['WS_F'].plot(ax = ax6, color = "green", linewidth = 0.5)
#SrmDF['SW_IN_F'].plot(ax = ax2, color = "green", linewidth = 0.5)
#SrgDF['SW_IN_F'].plot(ax = ax2, color = "darkblue", linewidth = 0.5)
ax6.set_ylim((0, 10))
ax6.yaxis.set_ticks(np.arange(0, 11, 2))
ax6.margins(y=0)
ax6.set_ylabel("Wind Speed \n (m/s)", fontsize = 10)
ax6.minorticks_off()
plt.savefig("SrgForcing.png", bbox_inches='tight', pad_inches = 0)




















