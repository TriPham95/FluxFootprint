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

FufFile = '/home/tpham/Desktop/ProcessedFiles/FufDiurnal_calibration.csv'
FufData = pd.read_csv(FufFile)





###############################################################################
FufData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FufData['Date']])
FufData.set_index('Time', inplace = True, drop = True)
FufData.replace(to_replace = -9999, value = np.nan, inplace = True) 

Start = np.where(FufData["Date"] == str('01/01/2006 00:00'))[0][0]
End = np.where(FufData["Date"] == str('12/31/2006 23:00'))[0][0]


plt.rcParams.update({'font.size': 22})
fig, ((ax1, ax2, ax3, ax4, ax5, ax6, ax7)) = plt.subplots(7, 1, figsize=(20,22))
fig.subplots_adjust(top=0.95)
FufData['Albedo'][Start:End].plot(ax=ax1, color = "black", linewidth = 4)
ax1.set_ylabel("Albedo []", fontsize = 22, fontweight = 'bold')
#ax1.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
ax1.get_xaxis().set_visible(False)

FufData['LAI'][Start:End].plot(ax=ax2, color = "black", linewidth = 4)
ax2.set_ylabel("LAI []", fontsize = 22, fontweight = 'bold')
#ax2.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax2.minorticks_off()
ax2.get_xaxis().set_visible(False)

FufData['VegFraction'][Start:End].plot(ax=ax3, color = "black", linewidth = 4)
ax3.set_ylabel(" VegFraction []", fontsize = 22, fontweight = 'bold')
#ax3.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax3.minorticks_off()
ax3.get_xaxis().set_visible(False)

FufData['OpticalTrans'][Start:End].plot(ax=ax4, color = "black", linewidth = 4)
ax4.set_ylabel("OpticalTrans []", fontsize = 22, fontweight = 'bold')
#ax4.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax4.minorticks_off()
ax4.get_xaxis().set_visible(False)

FufData['CanFieldCap'][Start:End].plot(ax=ax5, color = "black", linewidth = 4)
ax5.set_ylabel("CanFieldCap []", fontsize = 22, fontweight = 'bold')
#ax5.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax5.minorticks_off()
ax5.get_xaxis().set_visible(False)

FufData['ThroughFall'][Start:End].plot(ax=ax6, color = "black", linewidth = 4)
ax6.set_ylabel("Throughfall []", fontsize = 22, fontweight = 'bold')
#ax6.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax6.minorticks_off()
ax6.get_xaxis().set_visible(False)


FufData['StomRes'][Start:End].plot(ax=ax7, color = "black", linewidth = 4)
ax7.set_ylabel("StomRes [s/m]", fontsize = 22, fontweight = 'bold')
ax7.set_xlabel("Date", fontsize = 22, fontweight = 'bold')
ax7.minorticks_off()
#ax5.set_xticklabels([])

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Fuf_Forcing_Vegetation_2006_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)







































