#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 10:29:41 2020

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


###############################################################################
SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcData['TIMESTAMP_START']])
SrcData.set_index('Time', inplace = True, drop = True)
SrcData.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrcData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcData['TIMESTAMP_START']])
SrcData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcData['month']])
SrcData['month'].astype(float)
SrcDF = SrcData.apply(pd.to_numeric).resample("M").mean()
SrcDF['month'] = SrcDF['month'].astype(int)
###############################################################################
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData.set_index('Time', inplace = True, drop = True)
SrmData.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrmData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmData['TIMESTAMP_START']])
SrmData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmData['month']])
SrmData['month'].astype(float)
SrmDF = SrmData.apply(pd.to_numeric).resample("M").mean()
SrmDF['month'] = SrmDF['month'].astype(int)
###############################################################################
SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData.set_index('Time', inplace = True, drop = True)
SrgData.replace(to_replace = -9999, value = np.nan, inplace = True) 
SrgData['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgData['TIMESTAMP_START']])
SrgData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgData['month']])
SrmData['month'].astype(float)
SrgDF = SrgData.apply(pd.to_numeric).resample("M").mean()
SrgDF['month'] = SrgDF['month'].astype(int)
###############################################################################

line_labels = ["Creosote", "Mesquite", "Grassland"]

fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4, figsize=(38,18))
fig.subplots_adjust(top=0.95)
#fig.suptitle('Santa Rita Monthly Average Values from 2008 to 2014', fontsize = 16, fontweight = 'bold')
SrcDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax1, linewidth = 2)
SrmDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax1, linewidth = 2)
SrgDF.groupby(['month']).mean()['NETRAD'].plot(ax=ax1, linewidth = 2)
ax1.set_ylabel("Net Radiation [W/$\mathregular{m^2}$]", fontsize = 24, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax1.set_xticks(np.arange(1,13,1))
ax1.tick_params(axis='both', which='major', labelsize=24)
ax1.legend(labels = line_labels, fontsize = 24)

SrcDF.groupby(['month']).mean()['LE_F_MDS'].plot(ax=ax2, linewidth = 2)
SrmDF.groupby(['month']).mean()['LE_F_MDS'].plot(ax=ax2, linewidth = 2)
SrgDF.groupby(['month']).mean()['LE_F_MDS'].plot(ax=ax2, linewidth = 2)
ax2.set_ylabel("Latent Heat Flux [W/$\mathregular{m^2}$]", fontsize = 24, fontweight = 'bold')
ax2.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax2.set_xticks(np.arange(1,13,1))
ax2.tick_params(axis='both', which='major', labelsize=24)
ax2.legend(labels = line_labels, fontsize = 24)

SrcDF.groupby(['month']).mean()['H_F_MDS'].plot(ax=ax3, linewidth = 2)
SrmDF.groupby(['month']).mean()['H_F_MDS'].plot(ax=ax3, linewidth = 2)
SrgDF.groupby(['month']).mean()['H_F_MDS'].plot(ax=ax3, linewidth = 2)
ax3.set_ylabel("Sensible Heat Flux [W/$\mathregular{m^2}$]", fontsize = 24, fontweight = 'bold')
ax3.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax3.set_xticks(np.arange(1,13,1))
ax3.tick_params(axis='both', which='major', labelsize=24)
ax3.legend(labels = line_labels, fontsize = 24)

SrcDF.groupby(['month']).mean()['G_F_MDS'].plot(ax=ax4, linewidth = 2)
SrmDF.groupby(['month']).mean()['G_F_MDS'].plot(ax=ax4, linewidth = 2)
SrgDF.groupby(['month']).mean()['G_F_MDS'].plot(ax=ax4, linewidth = 2)
ax4.set_ylabel("Ground Heat Flux [W/$\mathregular{m^2}$]", fontsize = 24, fontweight = 'bold')
ax4.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax4.set_xticks(np.arange(1,13,1))
ax4.tick_params(axis='both', which='major', labelsize=24)
ax4.legend(labels = line_labels, fontsize = 24)

SrcDF.groupby(['month']).mean()['TS_1'].plot(ax=ax5, linewidth = 2)
SrmDF.groupby(['month']).mean()['TS_PI_1_1_A'].plot(ax=ax5, linewidth = 2)
SrgDF.groupby(['month']).mean()['TS_1_1_1'].plot(ax=ax5, linewidth = 2)
ax5.set_ylabel("Surface Temperature [$^\circ$C]", fontsize = 24, fontweight = 'bold')
ax5.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax5.set_xticks(np.arange(1,13,1))
ax5.tick_params(axis='both', which='major', labelsize=24)
ax5.legend(labels = line_labels, fontsize = 24)

SrcDF.groupby(['month']).mean()['TS_2'].plot(ax=ax6, linewidth = 2)
SrmDF.groupby(['month']).mean()['TS_PI_1_8_A'].plot(ax=ax6, linewidth = 2)
SrgDF.groupby(['month']).mean()['TS_1_6_1'].plot(ax=ax6, linewidth = 2)
ax6.set_ylabel("Rootzone Temperature [$^\circ$C]", fontsize = 24, fontweight = 'bold')
ax6.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax6.set_xticks(np.arange(1,13,1))
ax6.tick_params(axis='both', which='major', labelsize=24)
ax6.legend(labels = line_labels, fontsize = 24)

(SrcDF.groupby(['month']).mean()['SWC_1'] / 100).plot(ax=ax7, linewidth = 2)
(SrmDF.groupby(['month']).mean()['SWC_PI_1_1_A'] / 100).plot(ax=ax7, linewidth = 2)
(SrgDF.groupby(['month']).mean()['SWC_1_1_1'] / 100).plot(ax=ax7, linewidth = 2)
ax7.set_ylabel("Soil Moisture [ ]", fontsize = 24, fontweight = 'bold')
ax7.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax7.set_xticks(np.arange(1,13,1))
ax7.tick_params(axis='both', which='major', labelsize=24)
ax7.legend(labels = line_labels, fontsize = 24)

(SrcDF.groupby(['month']).mean()['SWC_2'] / 100).plot(ax=ax8, linewidth = 2)
(SrmDF.groupby(['month']).mean()['SWC_PI_1_7_A'] / 100).plot(ax=ax8, linewidth = 2)
(SrgDF.groupby(['month']).mean()['SWC_1_6_1'] / 100).plot(ax=ax8, linewidth = 2)
ax8.set_ylabel("Rootzone Moisture [ ]", fontsize = 24, fontweight = 'bold')
ax8.set_xlabel("Month", fontsize = 24, fontweight = 'bold')
ax8.set_xticks(np.arange(1,13,1))
ax8.tick_params(axis='both', which='major', labelsize=24)
ax8.legend(labels = line_labels, fontsize = 24)


plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SantaRitaMonthlyAverage.png", 
            bbox_inches='tight', pad_inches = 0.1)



















#ax = SrcDF.boxplot(column=['LE'], by = 'month')
#ax.grid(False)














