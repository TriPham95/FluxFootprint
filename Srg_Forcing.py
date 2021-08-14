#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 10:15:54 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime




SrgFile = '/home/tpham/Desktop/Tribs_USSrg_20082014/USSrg.csv'
SrgData = pd.read_csv(SrgFile, header = 0)


SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData.set_index('Time', inplace = True, drop = True)
Start = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
End = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 201001010000]).iloc[0].name)
SrgDF = SrgData[Start:End]
SrgDF.replace(to_replace = -9999, value = np.nan, inplace = True) 




###############################################################################
plt.rcParams.update({'font.size': 22})
fig, ((ax6, ax1, ax2, ax3, ax4, ax5)) = plt.subplots(6, 1, figsize=(20,18))
fig.subplots_adjust(top=0.95)

ax6.margins(y=0)
ax6.invert_yaxis()
ax6.set_ylim((0, 1))
ax6.set_ylim((41, 0))
ax6.yaxis.set_ticks(np.arange(0, 41, 10))
SrgData['P'].plot(ax=ax6,label = "Precipitation", color = 'black')
ax6.set_ylabel("P [mm]", fontsize = 22, fontweight = 'bold')
ax6.minorticks_off()
ax6.get_xaxis().set_visible(False)
#ax6.legend()


SrgData['SW_IN_F_MDS'][Start:End].plot(ax=ax1, label = "Shortwave Radiation", color = 'black')
ax1.set_ylabel("SW [W/$\mathregular{m^2}$]", fontsize = 22, fontweight = 'bold')
#ax1.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax1.minorticks_off()
ax1.get_xaxis().set_visible(False)
#ax1.legend()

SrgData['TA_F'][Start:End].plot(ax=ax2, label = "Air Temperature", color = 'black')
ax2.set_ylabel("TA [\xb0C]", fontsize = 22, fontweight = 'bold')
#ax2.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax2.minorticks_off()
ax2.get_xaxis().set_visible(False)
#ax2.legend()

SrgData['WS_F'][Start:End].plot(ax=ax3, label = "Wind Speed", color = 'black')
ax3.set_ylabel("WS [m/s]", fontsize = 22, fontweight = 'bold')
#ax3.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax3.minorticks_off()
ax3.get_xaxis().set_visible(False)
#ax3.legend()

(SrgData['PA_F']*10)[Start:End].plot(ax=ax4, label = "Air Pressure", color = 'black')
ax4.set_ylabel("PA [mbar]", fontsize = 22, fontweight = 'bold')
#ax4.set_xlabel("Year", fontsize = 14, fontweight = 'bold')
ax4.minorticks_off()
ax4.get_xaxis().set_visible(False)
#ax4.legend()

SrgData['RH'][Start:End].plot(ax=ax5, label = "Relative Humidity", color = 'black')
ax5.set_ylabel("RH [%]", fontsize = 22, fontweight = 'bold')
ax5.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax5.minorticks_off()
#ax5.set_xticklabels([])
#ax5.legend()

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/Srg_Forcing_2009_v2.png", 
            bbox_inches='tight', pad_inches = 0.1)


