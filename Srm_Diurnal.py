#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 11:18:13 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates



SrmFile = '/home/tpham/Desktop/ProcessedFiles/SrmDiurnal_validation.csv'
SrmData = pd.read_csv(SrmFile)





###############################################################################
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrmData['Date']])
SrmData.set_index('Time', inplace = True, drop = True)
SrmData.replace(to_replace = -9999, value = np.nan, inplace = True) 

Start = np.where(SrmData["Date"] == str('06/01/2010 00:00'))[0][0]
End = np.where(SrmData["Date"] == str('08/01/2010 01:00'))[0][0]

line_labels = ["Simulated", "Observed"]



###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ((ax6, ax4, ax1, ax2, ax3, ax5)) = plt.subplots(6, 1, figsize=(20,18))
fig.subplots_adjust(top=0.95)

ax6.margins(y=0)
ax6.invert_yaxis()
ax6.set_ylim((0, 1))
ax6.set_ylim((15, 0))
SrmData['Rain_Obs'].plot(ax=ax6, linewidth = 2, color = 'black')
ax6.set_ylabel("P [mm]", fontsize = 22, fontweight = 'bold')
ax6.minorticks_off()
ax6.get_xaxis().set_visible(False)
#ax6.legend(labels = "Precipitation")

SrmData['NetRad_Sim'][Start:End].plot(ax=ax4, color = 'red', linewidth = 2)
SrmData['NetRad_Obs'][Start:End].plot(ax=ax4, color = 'black', linewidth = 2)
ax4.set_ylabel("NR [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
#ax4.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax4.minorticks_off()
ax4.get_xaxis().set_visible(False)
#ax4.legend(labels = line_labels)

SrmData['LE_Sim'][Start:End].plot(ax=ax1, color = 'red', linewidth = 2)
SrmData['LE_Obs'][Start:End].plot(ax=ax1, color = 'black', linewidth = 2)
ax1.set_ylabel("LE [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
#ax1.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
ax1.get_xaxis().set_visible(False)
#ax1.legend(labels = line_labels)

SrmData['H_Sim'][Start:End].plot(ax=ax2, color = 'red', linewidth = 2)
SrmData['H_Obs'][Start:End].plot(ax=ax2, color = 'black', linewidth = 2)
ax2.set_ylabel("H [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
#ax2.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax2.minorticks_off()
ax2.get_xaxis().set_visible(False)
#ax2.legend(labels = line_labels)

SrmData['G_Sim'][Start:End].plot(ax=ax3, color = 'red', linewidth = 2)
SrmData['G_Obs'][Start:End].plot(ax=ax3, color = 'black', linewidth = 2)
ax3.set_ylabel("G [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
#ax3.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax3.minorticks_off()
ax3.get_xaxis().set_visible(False)
#ax3.legend(labels = line_labels)




ax5.plot(mdates.date2num(list(SrmData.index[Start:End])), SrmData['TS_Sim'][Start:End], color = 'red', linewidth = 2)
ax5.plot(mdates.date2num(list(SrmData.index[Start:End])), SrmData['TS_Obs'][Start:End], color = 'black', linewidth = 2)
ax5.set_ylabel("TS [\xb0C]", fontsize = 22, fontweight = 'bold')
ax5.set_xlabel("Date", fontsize = 22, fontweight = 'bold')
#ax5.minorticks_off()
#ax5.set_xticklabels([])

ax5.xaxis.set_major_locator(mdates.MonthLocator())
ax5.xaxis.set_major_formatter(mdates.DateFormatter('\n %b'))

ax5.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
ax5.xaxis.set_minor_locator(mdates.DayLocator(interval = 5))
ax5.legend(labels = line_labels, bbox_to_anchor=(0.75, -0.45), ncol = 2, frameon=False, fontsize = 22)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SrmDiurnal_2010_v3.pdf", 
            bbox_inches='tight', pad_inches = 0.1)






plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(figsize=(20,12))
fig.subplots_adjust(top=0.95)


lns1 = ax1.plot(mdates.date2num(list(SrmData.index)), SrmData['SoilMoisture_Sim'],
         label = 'Simulated SWC', linewidth = 4, color = 'red')

lns2 = ax1.plot(mdates.date2num(list(SrmData.index)), SrmData['SoilMoisture_Obs'],
         label = 'Observed SWC', linewidth = 4, color = 'black')


ax1.set_ylabel("Soil Moisture []", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.51, 0.1))
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.set_ylim((0, 0.8))
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)


ax2 = ax1.twinx()
ax2.invert_yaxis()
#FufDF_Daily['P_sum'].plot(ax = ax2, label = 'Precipitation (mm)')
lns3 = ax2.bar(mdates.date2num(list(SrmData.index)), SrmData['Rain_Obs'], 
        align = 'center', label = 'SRG Precipitation [mm]', width = 2)


ax2.margins(y=0)
ax2.set_ylim((30, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 11, 5))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))


plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = lns1+lns2+[lns3]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=7, frameon=False)



plt.savefig("/home/tpham/Windows Share/Thesis_Figures_2/SrmSWC_2010_v3.pdf", 
            bbox_inches='tight', pad_inches = 0.1)







