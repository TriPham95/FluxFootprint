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


SrgFile = '/home/tpham/Desktop/ProcessedFiles/SrgDiurnal_calibration_v2.csv'
LAIFile = '/home/tpham/Desktop/LAI_AZ.csv'

SrgData = pd.read_csv(SrgFile)
LAIData = pd.read_csv(LAIFile, header = 0)



###############################################################################
LAIData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in LAIData['Date ']])

LAIData.set_index('Time', inplace = True, drop = True)
LAIData.replace(to_replace = 'NA', value = np.nan, inplace = True) 


Start = LAIData.index.get_loc((LAIData[LAIData.index == '2009-01-01']).iloc[0].name)
End = LAIData.index.get_loc((LAIData[LAIData.index == '2009-12-31']).iloc[0].name)
LAIDF_AZ = LAIData[Start:End]

###############################################################################
SrgData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrgData['Date']])
SrgData.set_index('Time', inplace = True, drop = True)
SrgData.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrgData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrgData['Date']])
SrgData.drop(['Date'], axis = 1, inplace = True)
SrgData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgData['month']])
SrgDF = SrgData.apply(pd.to_numeric).resample("H").mean()
SrgDF['P_sum'] = SrgData['Rain_Obs'].apply(pd.to_numeric).resample("H").sum()


z1 = 0.1
z2 = 1


SrgDF = SrgDF[['TS_Sim', 'RootTS_Sim', 'SoilMoisture_Sim', 'RootSoilMoisture_Sim', 'LAI']]

SrgDF['SWC_avg'] = (SrgDF['SoilMoisture_Sim'] + SrgDF['RootSoilMoisture_Sim']) / 2


SrgDF['TS1_avg'] = SrgDF['TS_Sim'].resample('D').mean()
SrgDF['TS1_avg'] = SrgDF['TS1_avg'].fillna(method='ffill')

SrgDF['TS2_avg'] = SrgDF['RootTS_Sim'].resample('D').mean()
SrgDF['TS2_avg'] = SrgDF['TS2_avg'].fillna(method='ffill')



SrgDF['DampingDepth'] = ((z1 - z2) / 
     (np.log(np.abs(SrgDF['RootTS_Sim'] - SrgDF['TS2_avg'])) - 
      np.log(np.abs(SrgDF['TS_Sim'] - SrgDF['TS1_avg']))))


SrgDF['DampingDepth'][SrgDF['DampingDepth'] < 0] = 0.1
SrgDF['DampingDepth'][SrgDF['DampingDepth'] > 2.5] = 0.2

SrgDF = SrgDF.apply(pd.to_numeric).resample("D").mean()


SrgDF = SrgDF.merge(LAIDF_AZ['SrgLAI '], left_index=True, right_index=True, how='outer')
SrgDF['SrgLAI '] = SrgDF['SrgLAI '].fillna(method='ffill')

np.corrcoef(list(SrgDF['DampingDepth']), list(SrgDF['SrgLAI ']))[0, 1]
###############################################################################
# Calculate the point density
LAIDamp = np.vstack([SrgDF['SrgLAI '], SrgDF['DampingDepth']])
LAIDampDensity = gaussian_kde(LAIDamp)(LAIDamp)

# Sort the points by density, so that the densest points are plotted last
LAIDampScaled = LAIDampDensity.argsort()
x1, y1, LAIDampDensity = SrgDF['SrgLAI '][LAIDampScaled], SrgDF['DampingDepth'][LAIDampScaled], LAIDampDensity[LAIDampScaled]




SWCDamp = np.vstack([SrgDF['SWC_avg'], SrgDF['DampingDepth']])
SWCDampDensity = gaussian_kde(SWCDamp)(SWCDamp)

# Sort the points by density, so that the densest points are plotted last
SWCDampScaled = SWCDampDensity.argsort()
x2, y2, SWCDampDensity = SrgDF['SWC_avg'][SWCDampScaled], SrgDF['DampingDepth'][SWCDampScaled], SWCDampDensity[SWCDampScaled]


###############################################################################
m_LAI, b_LAI, r_LAI, p_LAI, std_LAI = stats.linregress(SrgDF['SrgLAI '], SrgDF['DampingDepth'])
line_LAI = m_LAI * SrgDF['SrgLAI '] + b_LAI


m_SWC, b_SWC, r_SWC, p_SWC, std_SWC = stats.linregress(SrgDF['SWC_avg'], SrgDF['DampingDepth'])
line_SWC = m_SWC * SrgDF['SWC_avg'] + b_SWC
###############################################################################



plt.rcParams.update({'font.size': 24})
plt.rcParams['axes.xmargin'] = 0
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26,12))
fig.subplots_adjust(top=0.95)



ax1.scatter(x1, y1, c=LAIDampDensity, s=50, edgecolor='', cmap='jet')
ax1.minorticks_off()
ax1.set_xlim((0, 1))
ax1.xaxis.set_ticks(np.arange(0, 1.01, 0.2))
ax1.set_ylim((0.2, 0.5))
ax1.yaxis.set_ticks(np.arange(0.2, 0.51, 0.1))
#ax1.plot([0, 1], [0, 1], transform=ax1.transAxes, color = 'black')
ax1.plot(SrgDF['SrgLAI '], line_LAI, 'r', 
         label='y={:.2f}x+{:.2f}, R2={:.2f}'.format(m_LAI, b_LAI, r_LAI))
ax1.set_ylabel("Damping Depth [m]", fontsize = 24, fontweight = 'bold')
ax1.set_xlabel("LAI []", fontsize = 24, fontweight = 'bold')
ax1.minorticks_off()
ax1.axis(option='square')

ax2.scatter(x2, y2, c=LAIDampDensity, s=50, edgecolor='', cmap='jet')
ax2.minorticks_off()
ax2.set_xlim((0, 0.2))
ax2.xaxis.set_ticks(np.arange(0, 0.21, 0.05))
ax2.set_ylim((0.2, 0.5))
ax2.yaxis.set_ticks(np.arange(0.2, 0.51, 0.1))
#ax2.plot([0, 1], [0, 1], transform=ax2.transAxes, color = 'black')
ax2.plot(SrgDF['SWC_avg'], line_SWC, 'r', 
         label='y={:.2f}x+{:.2f}, R2={:.2f}'.format(m_SWC, b_SWC, r_SWC))
ax2.set_ylabel("Damping Depth [m]", fontsize = 24, fontweight = 'bold')
ax2.set_xlabel("SWC []", fontsize = 24, fontweight = 'bold')
ax2.minorticks_off()
ax2.axis(option='square')
ax2.legend(frameon=False, fontsize = 26)
ax1.legend(frameon=False, fontsize = 26)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USSrg_DampingDepth_tRIBS_2009_v3.png", 
            bbox_inches='tight', pad_inches = 0.1)





np.corrcoef(list(SrgDF['DampingDepth']), list(SrgDF['LAI']))[0, 1]

np.corrcoef(list(SrgDF['DampingDepth']), list(SrgDF['SWC_avg']))[0, 1]














































