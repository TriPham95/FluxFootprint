#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 10:55:42 2019

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter



MoisstFile = '/home/tpham/Desktop/MOISSTFilled.csv'


MoisstData = pd.read_csv(MoisstFile)


MoisstData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in MoisstData['TIMESTAMP']])
MoisstData.drop(['TIMESTAMP'], axis = 1, inplace = True)
MoisstData.set_index('Time', inplace = True, drop = True)

MoisstData = MoisstData.astype('float32')
MoisstData.dropna()

# MoisstData['LE_wpl'][np.isfinite(MoisstData['LE_wpl'])].max()

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
MoisstData['SHF1_Avg'].plot(ax = ax1, color = "brown")
ax1.set_ylim((-50, 81))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-50, 81, 20))
ax1.margins(y=0)
ax1.set_ylabel("Soil Heat (W.m-2)", fontsize = 8)
#ax1.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')

MoisstData['LE_wpl'].plot(ax = ax2, color = "green")
ax2.set_ylim((-500, 601))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-500, 601, 200))
ax2.margins(y=0)
ax2.set_ylabel("Evapotrans (W.m-2)", fontsize = 8)

MoisstData['Hs'].plot(ax = ax3, color = "blue")
ax3.set_ylim((-500, 601))
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.yaxis.set_ticks(np.arange(-500, 601, 200))
ax3.margins(y=0)
ax3.set_ylabel("Sensible Heat (W.m-2)", fontsize = 8)

MoisstData['SoilTC1_Avg'].plot(ax = ax4, color = "orange")
ax4.set_ylim((0, 36))
ax4.set_xticklabels([])
ax4.xaxis.label.set_visible(False)
ax4.yaxis.set_ticks(np.arange(0, 36, 5))
ax4.margins(y=0)
ax4.set_ylabel("Soil Temperature (C)", fontsize = 8)

MoisstData['Rn_total_Avg'].plot(ax = ax5, color = "violet")
ax5.set_ylim((-100, 801))
#ax5.set_xticklabels([])
#ax5.xaxis.label.set_visible(False)
ax5.yaxis.set_ticks(np.arange(-100, 801, 200))
ax5.margins(y=0)
ax5.set_ylabel("Net Radiation (W.m-2)", fontsize = 8)














SWCFile = '/home/tpham/Windows Share/MOISST_SWC.csv'

SWCData = pd.read_csv(SWCFile)
SWCData.set_index('Time', inplace = True, drop = True)
SWCData = SWCData.astype('float32')
SWCData.dropna()

fig, ax = plt.subplots(1, 1)
plt.subplots_adjust(left = 0.125)
SWCData['SWC10cm'].plot(ax = ax)

#ax.plot(SWCData.index, SWCData['SWC10cm'])


date_form = DateFormatter("%m/%d")
ax.xaxis.set_major_formatter(date_form)





ax.set_ylim((81, 0))
ax.set_xticklabels([])
ax.xaxis.label.set_visible(False)
ax.yaxis.set_ticks(np.arange(0, 81, 20))
ax.margins(y=0)
ax.set_ylabel("Precipitation (mm)", fontsize = 8)
ax.xaxis.grid(True, which='major', linestyle=':', linewidth='0.5', color='black')



























