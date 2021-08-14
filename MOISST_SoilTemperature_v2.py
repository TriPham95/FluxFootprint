#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 19:08:09 2020

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

MoisstIndexStart = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201501010000]).iloc[0].name)
MoisstIndexEnd = MoisstData.index.get_loc((MoisstData[MoisstData['Timestamp'] == 201512310000]).iloc[0].name)

MoisstDF = MoisstData[MoisstIndexStart:(MoisstIndexEnd+1)]
MoisstDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

MoisstDF['Day'] = ([datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') 
                       for x in MoisstDF.index])




MoisstDF['Day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in MoisstDF['Day']])

MoisstDF = MoisstDF.apply(pd.to_numeric).resample("D").mean()


###############################################################################
MesonetFile = '/home/tpham/Desktop/ProcessedFiles/MoisstPrecipitation.csv'

MesonetData = pd.read_csv(MesonetFile)
MesonetData.replace(-999, float('nan'), inplace=True)

MesonetData['Time'] = ([datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M') 
                        for x in MesonetData['TIME']])
MesonetData['TAIR'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TAIR']])
MesonetData['TDEW'] = (["{0:.2f}".format((x - 32) * (5/9)) \
                       for x in MesonetData['TDEW']])
MesonetData['RELH'] = (["{0:.2f}".format(float(x) / 100) 
                        for x in MesonetData['RELH']])
MesonetData['RAIN'] = (["{0:.4f}".format(float(x) * 25.4) 
                        for x in MesonetData['RAIN']])
MesonetData['PRES'] = (["{0:.4f}".format(float(x) * 1) 
                        for x in MesonetData['PRES']])
MesonetData['SRAD'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['SRAD']])
MesonetData['WSPD'] = (["{0:.2f}".format(float(x) * 0.44704) 
                        for x in MesonetData['WSPD']])
MesonetData['WDIR'] = (["{0:.2f}".format(float(x)) 
                        for x in MesonetData['WDIR']])
MesonetData.drop(['STID', 'TIME', 'TMIN', 'TMAX', 'WMAX'], axis = 1, inplace = True)
MesonetData.set_index('Time', inplace = True, drop = True)
MesonetData = MesonetData.astype('float32')
Start = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-01-01 00:00:00']).iloc[0].name)
End = MesonetData.index.get_loc((MesonetData[MesonetData.index == '2015-12-31 23:00:00']).iloc[0].name)
MesonetData = MesonetData[Start:(End+1)]

MesonetData['Day'] = ([datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') 
                       for x in MesonetData.index])
MesonetData['Day'] = ([datetime.datetime.strftime(x, '%d') 
                        for x in MesonetData['Day']])

MesonetDF = MesonetData.apply(pd.to_numeric).resample("D").mean()
MesonetDF['P_sum'] = MesonetData['RAIN'].apply(pd.to_numeric).resample("D").sum()


MOISSTMerged = MesonetDF.merge(MoisstDF, left_index=True, right_index=True, how='outer')



Start = MOISSTMerged.index.get_loc((MOISSTMerged[MOISSTMerged.index == '2015-04-01']).iloc[0].name)
End = MOISSTMerged.index.get_loc((MOISSTMerged[MOISSTMerged.index == '2015-09-01']).iloc[0].name)

MOISSTMerged = MOISSTMerged[Start:End]


###############################################################################
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.xmargin'] = 0
fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
fig.subplots_adjust(top=0.95)


lns1 = ax1.plot(mdates.date2num(list(MOISSTMerged.index)), MOISSTMerged['SoilTC1_Avg'],
         label = 'Soil Temp 2.5 cm', linewidth = 4)

lns2 = ax1.plot(mdates.date2num(list(MOISSTMerged.index)), MOISSTMerged['SoilTC2_Avg'],
         label = 'Soil Temp 5 cm', linewidth = 4)

lns3 = ax1.plot(mdates.date2num(list(MOISSTMerged.index)), MOISSTMerged['SoilTC3_Avg'],
         label = 'Soil Temp 10 cm', linewidth = 4)

lns4 = ax1.plot(mdates.date2num(list(MOISSTMerged.index)), MOISSTMerged['SoilTC4_Avg'],
         label = 'Soil Temp 20 cm', linewidth = 4)

lns5 = ax1.plot(mdates.date2num(list(MOISSTMerged.index)), MOISSTMerged['SoilTC5_Avg'],
         label = 'Soil Temp 50 cm', linewidth = 4)

lns6 = ax1.plot(mdates.date2num(list(MOISSTMerged.index)), MOISSTMerged['SoilTC6_Avg'],
         label = 'Soil Temp 90 cm', linewidth = 4)

ax1.axvline(datetime.datetime(2015, 4, 20), color = "black", linewidth = 1)
ax2 = ax1.twinx()
ax2.invert_yaxis()

lns7 = ax2.bar(mdates.date2num(list(MOISSTMerged.index)), MOISSTMerged['P_sum'], 
        align = 'center', label = 'MOISST Precipitation [mm]', width = 2, color = 'black')



ax1.set_ylabel("Soil Temperature [\xb0C]", fontsize = 22, fontweight = 'bold')
ax1.set_xlabel("Month", fontsize = 22, fontweight = 'bold')
ax1.minorticks_off()

ax1.yaxis.set_ticks(np.arange(10, 31, 10))
ax1.yaxis.set_label_coords(-0.05,0.2)
ax1.set_ylim((10, 70))
ax1.set_xticklabels([])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.setp(ax1.get_xticklabels(), rotation=0)

ax2.margins(y=0)
ax2.set_ylim((150, 0))
ax2.set_ylabel("Precipitation [mm]", fontsize = 22, fontweight = 'bold', 
               rotation = 270, labelpad= 500)
ax2.yaxis.set_ticks(np.arange(0, 61, 10))
ax2.yaxis.set_label_coords(1.05, 0.85)
ax2.minorticks_off()
ax2.set_xticklabels([])
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.legend(prop={'size': 22})
ax1.legend(frameon=False)
ax2.legend().set_visible(False)


lns = lns1+lns2+lns3+lns4+lns5+lns6+[lns7]
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=7, frameon=False)

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/MOISSTSoilTemp_2015_v3.png", 
            bbox_inches='tight', pad_inches = 0.1)










































