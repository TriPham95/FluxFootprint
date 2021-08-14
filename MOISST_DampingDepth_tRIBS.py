#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 19:40:29 2020

@author: tpham
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from scipy.stats import gaussian_kde
from scipy import stats

MoisstFile = '/home/tpham/Desktop/ProcessedFiles/MoisstDiurnal_calibration_v2.csv'
LAIFile = '/home/tpham/Desktop/LAI_AZ.csv'

MoisstData = pd.read_csv(MoisstFile)
LAIData = pd.read_csv(LAIFile, header = 0)





###############################################################################
MoisstData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in MoisstData['Date']])
MoisstData.set_index('Time', inplace = True, drop = True)
MoisstData.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in MoisstData['Date']])
MoisstData.drop(['Date'], axis = 1, inplace = True)
MoisstData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in MoisstData['month']])
MoisstDF = MoisstData.apply(pd.to_numeric).resample("H").mean()
MoisstDF['P_sum'] = MoisstData['Rain_Obs'].apply(pd.to_numeric).resample("H").sum()


z1 = 0.1
z2 = 1


MoisstDF = MoisstDF[['TS_Sim', 'RootTS_Sim', 'SoilMoisture_Sim', 'RootSoilMoisture_Sim', 'LAI']]

MoisstDF['SWC_avg'] = (MoisstDF['SoilMoisture_Sim'] + MoisstDF['RootSoilMoisture_Sim']) / 2


MoisstDF['TS1_avg'] = MoisstDF['TS_Sim'].resample('D').mean()
MoisstDF['TS1_avg'] = MoisstDF['TS1_avg'].fillna(method='ffill')

MoisstDF['TS2_avg'] = MoisstDF['RootTS_Sim'].resample('D').mean()
MoisstDF['TS2_avg'] = MoisstDF['TS2_avg'].fillna(method='ffill')



MoisstDF['DampingDepth'] = ((z1 - z2) / 
     (np.log(np.abs(MoisstDF['RootTS_Sim'] - MoisstDF['TS2_avg'])) - 
      np.log(np.abs(MoisstDF['TS_Sim'] - MoisstDF['TS1_avg']))))


MoisstDF['DampingDepth'][MoisstDF['DampingDepth'] < 0] = 0.1
MoisstDF['DampingDepth'][MoisstDF['DampingDepth'] > 2.5] = 0.2

MoisstDF = MoisstDF.apply(pd.to_numeric).resample("D").mean()




np.corrcoef(list(MoisstDF['DampingDepth']), list(MoisstDF['LAI']))[0, 1]
###############################################################################
# Calculate the point density
LAIDamp = np.vstack([MoisstDF['LAI'], MoisstDF['DampingDepth']])
LAIDampDensity = gaussian_kde(LAIDamp)(LAIDamp)

# Sort the points by density, so that the densest points are plotted last
LAIDampScaled = LAIDampDensity.argsort()
x1, y1, LAIDampDensity = MoisstDF['LAI'][LAIDampScaled], MoisstDF['DampingDepth'][LAIDampScaled], LAIDampDensity[LAIDampScaled]




SWCDamp = np.vstack([MoisstDF['SWC_avg'], MoisstDF['DampingDepth']])
SWCDampDensity = gaussian_kde(SWCDamp)(SWCDamp)

# Sort the points by density, so that the densest points are plotted last
SWCDampScaled = SWCDampDensity.argsort()
x2, y2, SWCDampDensity = MoisstDF['SWC_avg'][SWCDampScaled], MoisstDF['DampingDepth'][SWCDampScaled], SWCDampDensity[SWCDampScaled]


###############################################################################
m_LAI, b_LAI, r_LAI, p_LAI, std_LAI = stats.linregress(MoisstDF['LAI'], MoisstDF['DampingDepth'])
line_LAI = m_LAI * MoisstDF['LAI'] + b_LAI


m_SWC, b_SWC, r_SWC, p_SWC, std_SWC = stats.linregress(MoisstDF['SWC_avg'], MoisstDF['DampingDepth'])
line_SWC = m_SWC * MoisstDF['SWC_avg'] + b_SWC
###############################################################################



plt.rcParams.update({'font.size': 24})
plt.rcParams['axes.xmargin'] = 0
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26,12))
fig.subplots_adjust(top=0.95)



ax1.scatter(x1, y1, c=LAIDampDensity, s=50, edgecolor='', cmap='jet')
ax1.minorticks_off()
ax1.set_xlim((0, 3.5))
ax1.xaxis.set_ticks(np.arange(0, 3.51, 0.5))
ax1.set_ylim((0.2, 0.6))
ax1.yaxis.set_ticks(np.arange(0.2, 0.61, 0.1))
#ax1.plot([0, 1], [0, 1], transform=ax1.transAxes, color = 'black')
ax1.plot(MoisstDF['LAI'], line_LAI, 'r', 
         label='y={:.2f}x+{:.2f}, R2={:.2f}'.format(m_LAI, b_LAI, r_LAI))
ax1.set_ylabel("Damping Depth [m]", fontsize = 24, fontweight = 'bold')
ax1.set_xlabel("LAI []", fontsize = 24, fontweight = 'bold')
ax1.minorticks_off()
ax1.axis(option='square')

ax2.scatter(x2, y2, c=LAIDampDensity, s=50, edgecolor='', cmap='jet')
ax2.minorticks_off()
ax2.set_xlim((0, 0.6))
ax2.xaxis.set_ticks(np.arange(0, 0.61, 0.1))
ax2.set_ylim((0.2, 0.6))
ax2.yaxis.set_ticks(np.arange(0.2, 0.61, 0.1))
#ax2.plot([0, 1], [0, 1], transform=ax2.transAxes, color = 'black')
ax2.plot(MoisstDF['SWC_avg'], line_SWC, 'r', 
         label='y={:.2f}x+{:.2f}, R2={:.2f}'.format(m_SWC, b_SWC, r_SWC))
ax2.set_ylabel("Damping Depth [m]", fontsize = 24, fontweight = 'bold')
ax2.set_xlabel("SWC []", fontsize = 24, fontweight = 'bold')
ax2.minorticks_off()
ax2.axis(option='square')
ax2.legend(frameon=False, fontsize = 26)
ax1.legend(frameon=False, fontsize = 26)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USMoisst_DampingDepth_tRIBS_2016_v3.png", 
            bbox_inches='tight', pad_inches = 0.1)




np.corrcoef(list(MoisstDF['DampingDepth']), list(MoisstDF['LAI']))[0, 1]

np.corrcoef(list(MoisstDF['DampingDepth']), list(MoisstDF['SWC_avg']))[0, 1]















































