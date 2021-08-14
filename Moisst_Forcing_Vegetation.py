#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:22:35 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates

MoisstFile = '/home/tpham/Desktop/ProcessedFiles/MoisstDiurnal_calibration.csv'
MoisstData = pd.read_csv(MoisstFile)





###############################################################################
MoisstData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in MoisstData['Date']])
MoisstData.set_index('Time', inplace = True, drop = True)
MoisstData.replace(to_replace = -9999, value = np.nan, inplace = True) 

Start = np.where(MoisstData["Date"] == str('01/01/2016 00:00'))[0][0]
End = np.where(MoisstData["Date"] == str('12/31/2016 01:00'))[0][0]


###############################################################################
plt.rcParams.update({'font.size': 22})
fig, ((ax1, ax2, ax3, ax4, ax5, ax6, ax7)) = plt.subplots(7, 1, figsize=(20,22))
fig.subplots_adjust(top=0.95)
#fig.suptitle('Flagstaff Monthly Average Values from 2006 to 2010', fontsize = 14, fontweight = 'bold')
MoisstData['Albedo'][Start:End].plot(ax=ax1, color = "black", linewidth = 4)
ax1.set_ylabel("Albedo []", fontsize = 22, fontweight = 'bold')
#ax1.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
ax1.get_xaxis().set_visible(False)

MoisstData['LAI'][Start:End].plot(ax=ax2, color = "black", linewidth = 4)
ax2.set_ylabel("LAI []", fontsize = 22, fontweight = 'bold')
#ax2.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax2.minorticks_off()
ax2.get_xaxis().set_visible(False)

MoisstData['VegFraction'][Start:End].plot(ax=ax3, color = "black", linewidth = 4)
ax3.set_ylabel(" VegFraction []", fontsize = 22, fontweight = 'bold')
#ax3.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax3.minorticks_off()
ax3.get_xaxis().set_visible(False)

MoisstData['OpticalTrans'][Start:End].plot(ax=ax4, color = "black", linewidth = 4)
ax4.set_ylabel("OpticalTrans []", fontsize = 22, fontweight = 'bold')
#ax4.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax4.minorticks_off()
ax4.get_xaxis().set_visible(False)

MoisstData['CanFieldCap'][Start:End].plot(ax=ax5, color = "black", linewidth = 4)
ax5.set_ylabel("CanFieldCap []", fontsize = 22, fontweight = 'bold')
#ax5.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax5.minorticks_off()
ax5.get_xaxis().set_visible(False)

MoisstData['ThroughFall'][Start:End].plot(ax=ax6, color = "black", linewidth = 4)
ax6.set_ylabel("Throughfall []", fontsize = 22, fontweight = 'bold')
#ax6.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax6.minorticks_off()
ax6.get_xaxis().set_visible(False)


MoisstData['StomRes'][Start:End].plot(ax=ax7, color = "black", linewidth = 4)
ax7.set_ylabel("StomRes [s/m]", fontsize = 22, fontweight = 'bold')
ax7.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax7.minorticks_off()
ax7.xaxis.set_major_locator(mdates.MonthLocator())
ax7.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax7.get_xticklabels(), rotation=0)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Moisst_Forcing_Vegetation_2016_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)







































