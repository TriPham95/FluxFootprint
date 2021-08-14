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

FmfFile = '/home/tpham/Desktop/ProcessedFiles/FmfDiurnal_validation_v2.csv'
LAIFile = '/home/tpham/Desktop/LAI_AZ.csv'

FmfData = pd.read_csv(FmfFile)
LAIData = pd.read_csv(LAIFile, header = 0)



###############################################################################
LAIData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d') 
                        for x in LAIData['Date ']])

LAIData.set_index('Time', inplace = True, drop = True)
LAIData.replace(to_replace = 'NA', value = np.nan, inplace = True) 


Start = LAIData.index.get_loc((LAIData[LAIData.index == '2010-01-01']).iloc[0].name)
End = LAIData.index.get_loc((LAIData[LAIData.index == '2010-12-31']).iloc[0].name)
LAIDF_AZ = LAIData[Start:End]

###############################################################################
FmfData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FmfData['Date']])
FmfData.set_index('Time', inplace = True, drop = True)
FmfData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FmfData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in FmfData['Date']])
FmfData.drop(['Date'], axis = 1, inplace = True)
FmfData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FmfData['month']])
FmfDF = FmfData.apply(pd.to_numeric).resample("H").mean()
FmfDF['P_sum'] = FmfData['Rain_Obs'].apply(pd.to_numeric).resample("H").sum()


z1 = 0.1
z2 = 1


FmfDF = FmfDF[['TS_Sim', 'RootTS_Sim', 'SoilMoisture_Sim', 'RootSoilMoisture_Sim', 'LAI']]

FmfDF['SWC_avg'] = (FmfDF['SoilMoisture_Sim'] + FmfDF['RootSoilMoisture_Sim']) / 2


FmfDF['TS1_avg'] = FmfDF['TS_Sim'].resample('D').mean()
FmfDF['TS1_avg'] = FmfDF['TS1_avg'].fillna(method='ffill')

FmfDF['TS2_avg'] = FmfDF['RootTS_Sim'].resample('D').mean()
FmfDF['TS2_avg'] = FmfDF['TS2_avg'].fillna(method='ffill')



FmfDF['DampingDepth'] = ((z1 - z2) / 
     (np.log(np.abs(FmfDF['RootTS_Sim'] - FmfDF['TS2_avg'])) - 
      np.log(np.abs(FmfDF['TS_Sim'] - FmfDF['TS1_avg']))))


FmfDF['DampingDepth'][FmfDF['DampingDepth'] < 0] = 0.1
FmfDF['DampingDepth'][FmfDF['DampingDepth'] > 2.5] = 0.2

FmfDF = FmfDF.apply(pd.to_numeric).resample("D").mean()


FmfDF = FmfDF.merge(LAIDF_AZ['FmfLAI '], left_index=True, right_index=True, how='outer')

np.corrcoef(list(FmfDF['DampingDepth']), list(FmfDF['LAI']))[0, 1]
###############################################################################
# Calculate the point density
LAIDamp = np.vstack([FmfDF['LAI'], FmfDF['DampingDepth']])
LAIDampDensity = gaussian_kde(LAIDamp)(LAIDamp)

# Sort the points by density, so that the densest points are plotted last
LAIDampScaled = LAIDampDensity.argsort()
x1, y1, LAIDampDensity = FmfDF['LAI'][LAIDampScaled], FmfDF['DampingDepth'][LAIDampScaled], LAIDampDensity[LAIDampScaled]




SWCDamp = np.vstack([FmfDF['SWC_avg'], FmfDF['DampingDepth']])
SWCDampDensity = gaussian_kde(SWCDamp)(SWCDamp)

# Sort the points by density, so that the densest points are plotted last
SWCDampScaled = SWCDampDensity.argsort()
x2, y2, SWCDampDensity = FmfDF['SWC_avg'][SWCDampScaled], FmfDF['DampingDepth'][SWCDampScaled], SWCDampDensity[SWCDampScaled]

###############################################################################
m_LAI, b_LAI, r_LAI, p_LAI, std_LAI = stats.linregress(FmfDF['LAI'], FmfDF['DampingDepth'])
line_LAI = m_LAI * FmfDF['LAI'] + b_LAI


m_SWC, b_SWC, r_SWC, p_SWC, std_SWC = stats.linregress(FmfDF['SWC_avg'], FmfDF['DampingDepth'])
line_SWC = m_SWC * FmfDF['SWC_avg'] + b_SWC
###############################################################################




plt.rcParams.update({'font.size': 24})
plt.rcParams['axes.xmargin'] = 0
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26,12))
fig.subplots_adjust(top=0.95)



ax1.scatter(x1, y1, c=LAIDampDensity, s=50, edgecolor='', cmap='jet')
ax1.minorticks_off()
ax1.set_xlim((0, 2.5))
ax1.xaxis.set_ticks(np.arange(0, 2.51, 0.5))
ax1.set_ylim((0.2, 0.6))
ax1.yaxis.set_ticks(np.arange(0.2, 0.61, 0.1))
#ax1.plot([0, 1], [0, 1], transform=ax1.transAxes, color = 'black')
ax1.plot(FmfDF['LAI'], line_LAI, 'r', 
         label='y={:.2f}x+{:.2f}, R2={:.2f}'.format(m_LAI, b_LAI, r_LAI))
ax1.set_ylabel("Damping Depth [m]", fontsize = 24, fontweight = 'bold')
ax1.set_xlabel("LAI []", fontsize = 24, fontweight = 'bold')
ax1.minorticks_off()
ax1.axis(option='square')

ax2.scatter(x2, y2, c=LAIDampDensity, s=50, edgecolor='', cmap='jet')
ax2.minorticks_off()
ax2.set_xlim((0, 0.5))
ax2.xaxis.set_ticks(np.arange(0, 0.51, 0.1))
ax2.set_ylim((0.2, 0.6))
ax2.yaxis.set_ticks(np.arange(0.2, 0.61, 0.1))
#ax2.plot([0, 1], [0, 1], transform=ax2.transAxes, color = 'black')
ax2.plot(FmfDF['SWC_avg'], line_SWC, 'r', 
         label='y={:.2f}x+{:.2f}, R2={:.2f}'.format(m_SWC, b_SWC, r_SWC))
ax2.set_ylabel("Damping Depth [m]", fontsize = 24, fontweight = 'bold')
ax2.set_xlabel("SWC []", fontsize = 24, fontweight = 'bold')
ax2.minorticks_off()
ax2.axis(option='square')

ax1.legend(frameon=False, fontsize = 26)
ax2.legend(frameon=False, fontsize = 26)


plt.savefig("/home/tpham/Windows Share/Thesis_Figures/USFmf_DampingDepth_tRIBS_2010_v3.png", 
            bbox_inches='tight', pad_inches = 0.1)




np.corrcoef(list(FmfDF['DampingDepth']), list(FmfDF['LAI']))[0, 1]

np.corrcoef(list(FmfDF['DampingDepth']), list(FmfDF['SWC_avg']))[0, 1]















































