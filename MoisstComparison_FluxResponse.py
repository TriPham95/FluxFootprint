#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:37:43 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec


MoisstFile = '/home/tpham/Desktop/ProcessedFiles/MoisstFormatted.csv'
MoisstData = pd.read_csv(MoisstFile)

MoisstData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in MoisstData['Timestamp']])
MoisstData.set_index('Time', inplace = True, drop = True)

#MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201504010000]).iloc[0].name)
#MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201505200000]).iloc[0].name)

MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201504010000]).iloc[0].name)
MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201505200000]).iloc[0].name)

MoisstDF = MoisstData[MoisstIndexStart:(MoisstIndexEnd+1)]
MoisstDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstDF['Day'] = ([datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') 
                       for x in MoisstDF.index])




MoisstDF['Day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in MoisstDF['Day']])

#MoisstDF = MoisstDF.apply(pd.to_numeric).resample("H").mean()









###############################################################################

# Fluxes
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.labelweight'] = 'bold'
fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(8, 1, figsize=(20, 34))
fig.subplots_adjust(top = 0.95)

plt.minorticks_off()
MoisstDF['Rn_total_Avg'].plot(ax = ax1, linewidth = 4, color = 'black')
ax1.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax1.set_ylim((-200, 800))
ax1.set_xticklabels([])
ax1.xaxis.label.set_visible(False)
ax1.yaxis.set_ticks(np.arange(-200, 801, 200))
ax1.margins(y=0)
ax1.set_ylabel("NETRAD [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax1.get_xaxis().set_visible(False)
ax1.minorticks_off()


MoisstDF['LE_wpl'].plot(ax = ax2, linewidth = 4, color = 'black')
ax2.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax2.set_ylim((-100, 400))
ax2.set_xticklabels([])
ax2.xaxis.label.set_visible(False)
ax2.yaxis.set_ticks(np.arange(-100, 401, 100))
ax2.margins(y=0)
ax2.set_ylabel("LE [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax2.get_xaxis().set_visible(False)
ax2.minorticks_off()

MoisstDF['Hs'].plot(ax = ax3, linewidth = 4, color = 'black')
ax3.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax3.set_ylim((-200, 400))
ax3.set_xticklabels([])
ax3.xaxis.label.set_visible(False)
ax3.yaxis.set_ticks(np.arange(-200, 401, 100))
ax3.margins(y=0)
ax3.set_ylabel("H [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax3.get_xaxis().set_visible(False)
ax3.minorticks_off()

MoisstDF['SHF1_Avg'].plot(ax = ax4, linewidth = 4, color = 'black')
ax4.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax4.set_ylim((-100, 400))
ax4.yaxis.set_ticks(np.arange(-100, 401, 100))
ax4.margins(y=0)
ax4.set_ylabel("G [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
ax4.set_xlabel("Time", fontsize = 22, fontweight = 'bold')
ax4.get_xaxis().set_visible(False)
ax4.minorticks_off()


plt.minorticks_off()
MoisstDF['SWC5'].plot(ax = ax5, linewidth = 4, color = 'black')
ax5.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax5.set_ylim((0, 0.8))
ax5.set_xticklabels([])
ax5.xaxis.label.set_visible(False)
ax5.yaxis.set_ticks(np.arange(0, 0.81, 0.2))
ax5.margins(y=0)
ax5.set_ylabel("SWC10 [ ]", fontsize = 22, fontweight = 'bold')
ax5.get_xaxis().set_visible(False)
ax5.minorticks_off()


MoisstDF['SWC90'].plot(ax = ax6, linewidth = 4, color = 'black')
ax6.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax6.set_ylim((0.0, 0.8))
ax6.set_xticklabels([])
ax6.xaxis.label.set_visible(False)
ax6.yaxis.set_ticks(np.arange(0, 0.81, 0.2))
ax6.margins(y=0)
ax6.set_ylabel("SWC90 [ ]", fontsize = 22, fontweight = 'bold')
ax6.get_xaxis().set_visible(False)
ax6.minorticks_off()


MoisstDF['SoilTC1_Avg'].plot(ax = ax7, linewidth = 4, color = 'black')
ax7.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
ax7.set_ylim((10, 30))
ax7.yaxis.set_ticks(np.arange(10, 31, 10))
ax7.set_xticklabels([])
ax7.xaxis.label.set_visible(False)
ax7.margins(y=0)
ax7.set_ylabel(" Tsoil5 [\xb0C]", fontsize = 22, fontweight = 'bold')
ax7.get_xaxis().set_visible(False)
ax7.minorticks_off()


MoisstDF['SoilTC6_Avg'].plot(ax = ax8, linewidth = 4, color = 'black')
ax8.axvline(datetime.datetime(2015, 4, 20), color = "C1", linewidth = 1)
#ax8.axvline(datetime.datetime(2015, 2, 9), color = "#e377c2", linewidth = 0.25)
ax8.set_ylim((10, 30))
ax8.yaxis.set_ticks(np.arange(10, 31, 10))
ax8.margins(y=0)
ax8.set_ylabel(" TSoil90 [\xb0C]", fontsize = 22, fontweight = 'bold')
ax8.set_xlabel("Date", fontsize = 22, fontweight = 'bold')


#ax8.xaxis.set_major_locator(mdates.MonthLocator())
#ax8.xaxis.set_major_formatter(mdates.MonthFormatter('%b'))
#ax8.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
#ax8.xaxis.set_minor_locator(mdates.DayLocator(interval = 48))


labels = [item.get_text() for item in ax8.get_xticklabels()]


plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Moisst_FluxResponses_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)





















