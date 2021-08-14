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

SrmFile = '/home/tpham/Desktop/ProcessedFiles/SrmDiurnal_calibration_v2.csv'
LAIFile = '/home/tpham/Desktop/LAI_AZ.csv'

SrmData = pd.read_csv(SrmFile)
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
SrmData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrmData['Date']])
SrmData.set_index('Time', inplace = True, drop = True)
SrmData.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrmData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrmData['Date']])
SrmData.drop(['Date'], axis = 1, inplace = True)
SrmData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmData['month']])
SrmDF = SrmData.apply(pd.to_numeric).resample("H").mean()
SrmDF['P_sum'] = SrmData['Rain_Obs'].apply(pd.to_numeric).resample("H").sum()


z1 = 0.1
z2 = 1


SrmDF = SrmDF[['TS_Sim', 'RootTS_Sim', 'SoilMoisture_Sim', 'RootSoilMoisture_Sim', 'LAI']]

SrmDF['SWC_avg'] = (SrmDF['SoilMoisture_Sim'] + SrmDF['RootSoilMoisture_Sim']) / 2


SrmDF['TS1_avg'] = SrmDF['TS_Sim'].resample('D').mean()
SrmDF['TS1_avg'] = SrmDF['TS1_avg'].fillna(method='ffill')

SrmDF['TS2_avg'] = SrmDF['RootTS_Sim'].resample('D').mean()
SrmDF['TS2_avg'] = SrmDF['TS2_avg'].fillna(method='ffill')



SrmDF['DampingDepth'] = ((z1 - z2) / 
     (np.log(np.abs(SrmDF['RootTS_Sim'] - SrmDF['TS2_avg'])) - 
      np.log(np.abs(SrmDF['TS_Sim'] - SrmDF['TS1_avg']))))


SrmDF['DampingDepth'][SrmDF['DampingDepth'] < 0] = 0.1
SrmDF['DampingDepth'][SrmDF['DampingDepth'] > 2.5] = 0.2

SrmDF = SrmDF.apply(pd.to_numeric).resample("D").mean()


SrmDF = SrmDF.merge(LAIDF_AZ['SrmLAI'], left_index=True, right_index=True, how='outer')
SrmDF['SrmLAI'] = SrmDF['SrmLAI'].fillna(method='ffill')



np.corrcoef(list(SrmDF['DampingDepth']), list(SrmDF['SrmLAI']))[0, 1]
###############################################################################
# Calculate the point density
LAIDamp = np.vstack([SrmDF['SrmLAI'], SrmDF['DampingDepth']])
LAIDampDensity = gaussian_kde(LAIDamp)(LAIDamp)

# Sort the points by density, so that the densest points are plotted last
LAIDampScaled = LAIDampDensity.argsort()
x1, y1, LAIDampDensity = SrmDF['SrmLAI'][LAIDampScaled], SrmDF['DampingDepth'][LAIDampScaled], LAIDampDensity[LAIDampScaled]




SWCDamp = np.vstack([SrmDF['SWC_avg'], SrmDF['DampingDepth']])
SWCDampDensity = gaussian_kde(SWCDamp)(SWCDamp)

# Sort the points by density, so that the densest points are plotted last
SWCDampScaled = SWCDampDensity.argsort()
x2, y2, SWCDampDensity = SrmDF['SWC_avg'][SWCDampScaled], SrmDF['DampingDepth'][SWCDampScaled], SWCDampDensity[SWCDampScaled]


###############################################################################
m_LAI, b_LAI, r_LAI, p_LAI, std_LAI = stats.linregress(SrmDF['SrmLAI'], SrmDF['DampingDepth'])
line_LAI = m_LAI * SrmDF['SrmLAI'] + b_LAI


m_SWC, b_SWC, r_SWC, p_SWC, std_SWC = stats.linregress(SrmDF['SWC_avg'], SrmDF['DampingDepth'])
line_SWC = m_SWC * SrmDF['SWC_avg'] + b_SWC
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
ax1.plot(SrmDF['SrmLAI'], line_LAI, 'r', 
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
ax2.plot(SrmDF['SWC_avg'], line_SWC, 'r', 
         label='y={:.3f}x+{:.2f}, R2={:.2f}'.format(m_SWC, b_SWC, r_SWC))
ax2.set_ylabel("Damping Depth [m]", fontsize = 24, fontweight = 'bold')
ax2.set_xlabel("SWC []", fontsize = 24, fontweight = 'bold')
ax2.minorticks_off()
ax2.axis(option='square')
ax1.legend(frameon=False, fontsize = 26)
ax2.legend(frameon=False, fontsize = 26)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USSrm_DampingDepth_tRIBS_2009_v3.png", 
            bbox_inches='tight', pad_inches = 0.1)





np.corrcoef(list(SrmDF['DampingDepth']), list(SrmDF['LAI']))[0, 1]
















































