#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:03:50 2020

@author: tpham
"""


import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime


SrgFile = '/home/tpham/Desktop/ProcessedFiles/SrgDiurnal_validation.csv'
SrmFile = '/home/tpham/Desktop/ProcessedFiles/SrmDiurnal_validation.csv'
SrcFile = '/home/tpham/Desktop/ProcessedFiles/SrcDiurnal_validation.csv'


SrgData = pd.read_csv(SrgFile)
SrmData = pd.read_csv(SrmFile)
SrcData = pd.read_csv(SrcFile)

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
SrgData = SrgData.apply(pd.to_numeric).resample("M").mean()
SrgData['month'] = SrgData['month'].astype(int)
SrgData = SrgData.apply(pd.to_numeric).resample("M").mean()
SrgData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrgData.index])

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
SrmData = SrmData.apply(pd.to_numeric).resample("M").mean()
SrmData['month'] = SrmData['month'].astype(int)
SrmData = SrmData.apply(pd.to_numeric).resample("M").mean()
SrmData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrmData.index])

###############################################################################
SrcData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in SrcData['Date']])
SrcData.set_index('Time', inplace = True, drop = True)
SrcData.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrcData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in SrcData['Date']])
SrcData.drop(['Date'], axis = 1, inplace = True)
SrcData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcData['month']])
SrcData = SrcData.apply(pd.to_numeric).resample("M").mean()
SrcData['month'] = SrcData['month'].astype(int)
SrcData = SrcData.apply(pd.to_numeric).resample("M").mean()
SrcData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrcData.index])


###############################################################################
SrgFlux = '/home/tpham/Desktop/ProcessedFiles/USSrgFormatted.csv'
SrgFluxData = pd.read_csv(SrgFlux, header = 0)
SrgFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgFluxData['Timestamp']])
SrgFluxData.set_index('Time', inplace = True, drop = True)
Start = SrgFluxData.index.get_loc((SrgFluxData[SrgFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = SrgFluxData.index.get_loc((SrgFluxData[SrgFluxData['Timestamp'] == 201012312300]).iloc[0].name)
SrgFluxDF = SrgFluxData[Start:End]
SrgFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrgFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrgFluxDF['Timestamp']])
SrgFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrgFluxDF['month']])
SrgFluxDF['month'].astype(float)
SrgFluxDF = SrgFluxDF.apply(pd.to_numeric).resample("M").sum()
SrgFluxDF['month'] = SrgFluxDF['month'].astype(int)

SrgFluxDF = SrgFluxDF[['P_F']]

SrgFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrgFluxDF.index])

SrgParition = SrgData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]
SrgParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)



fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
SrgParition.plot.area(stacked = True, ax = ax1)
ax1.set_ylim((0, 0.4))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.21, 0.1))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 14, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)
ax2 = ax1.twinx()
ax2.invert_yaxis()
SrgFluxDF['P_F'].plot.bar(ax=ax2, width = 0.1)
plt.xlim([0,11])
#plt.xlim([0,SrgParition.size])
ax2.set_ylim((300, 0))
ax2.yaxis.set_ticks(np.arange(0, 81, 10))
ax2.set_ylabel("Precipitation [mm]", fontsize = 14, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.legend(loc = 'center right', fancybox = True, framealpha = 0.5,prop = {'size': 14})
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')

#plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SrgPartition_2010_v2.png", 
#            bbox_inches='tight', pad_inches = 0.1)































































'''
###############################################################################
SrcFlux = '/home/tpham/Desktop/Tribs_USSrc_20082014/USSrcFormatted.csv'
SrcFluxData = pd.read_csv(SrcFlux, header = 0)
SrcFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcFluxData['Timestamp']])
SrcFluxData.set_index('Time', inplace = True, drop = True)
Start = SrcFluxData.index.get_loc((SrcFluxData[SrcFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = SrcFluxData.index.get_loc((SrcFluxData[SrcFluxData['Timestamp'] == 201012312300]).iloc[0].name)
SrcFluxDF = SrcFluxData[Start:End]
SrcFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrcFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrcFluxDF['Timestamp']])
SrcFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrcFluxDF['month']])
SrcFluxDF['month'].astype(float)
SrcFluxDF = SrcFluxDF.apply(pd.to_numeric).resample("M").sum()
SrcFluxDF['month'] = SrcFluxDF['month'].astype(int)

SrcFluxDF = SrcFluxDF[['P_F']]
SrcFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrcFluxDF.index])


SrcParition = SrcData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

SrcParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)

fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
SrcParition.plot.area(stacked = True, ax = ax1)
ax1.set_ylim((0, 0.4))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.21, 0.1))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 14, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)
ax2 = ax1.twinx()
ax2.invert_yaxis()
SrcFluxDF['P_F'].plot.bar(ax=ax2, width = 0.1)
plt.xlim([0,11])
#plt.xlim([0,SrgParition.size])
ax2.set_ylim((300, 0))
ax2.yaxis.set_ticks(np.arange(0, 81, 10))
ax2.set_ylabel("Precipitation [mm]", fontsize = 14, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.legend(loc = 'center right', fancybox = True, framealpha = 0.5,prop = {'size': 14})
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SrcPartition_2010.png", 
            bbox_inches='tight', pad_inches = 0.1)




###############################################################################
SrmFlux = '/home/tpham/Desktop/Tribs_USSrm_20082014/USSrmFormatted.csv'
SrmFluxData = pd.read_csv(SrmFlux, header = 0)
SrmFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmFluxData['Timestamp']])
SrmFluxData.set_index('Time', inplace = True, drop = True)
Start = SrmFluxData.index.get_loc((SrmFluxData[SrmFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = SrmFluxData.index.get_loc((SrmFluxData[SrmFluxData['Timestamp'] == 201012312300]).iloc[0].name)
SrmFluxDF = SrmFluxData[Start:End]
SrmFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True)


SrmFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in SrmFluxDF['Timestamp']])
SrmFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in SrmFluxDF['month']])
SrmFluxDF['month'].astype(float)
SrmFluxDF = SrmFluxDF.apply(pd.to_numeric).resample("M").sum()
SrmFluxDF['month'] = SrmFluxDF['month'].astype(int)

SrmFluxDF = SrmFluxDF[['P_F']]
SrmFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in SrmFluxDF.index])

SrmParition = SrmData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

SrmParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)



fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
SrmParition.plot.area(stacked = True, ax = ax1)
ax1.set_ylim((0, 0.4))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.21, 0.1))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 14, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.3)
ax2 = ax1.twinx()
ax2.invert_yaxis()
SrmFluxDF['P_F'].plot.bar(ax=ax2, width = 0.1)
plt.xlim([0,11])
#plt.xlim([0,SrgParition.size])
ax2.set_ylim((300, 0))
ax2.yaxis.set_ticks(np.arange(0, 81, 10))
ax2.set_ylabel("Precipitation [mm]", fontsize = 14, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.legend(loc = 'center right', fancybox = True, framealpha = 0.5,prop = {'size': 14})
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SrmPartition_2010.png", 
            bbox_inches='tight', pad_inches = 0.1)


'''



















