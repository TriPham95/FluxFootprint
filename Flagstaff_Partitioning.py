#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:06:06 2020

@author: tpham
"""



import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import datetime


FufFile = '/home/tpham/Desktop/FufDiurnal_validation.csv'
FwfFile = '/home/tpham/Desktop/FwfDiurnal_calibration.csv'


FufData = pd.read_csv(FufFile)
FwfData = pd.read_csv(FwfFile)

###############################################################################
FufData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FufData['Date']])
FufData.set_index('Time', inplace = True, drop = True)
FufData.replace(to_replace = -9999, value = np.nan, inplace = True) 
FufData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in FufData['Date']])
FufData.drop(['Date'], axis = 1, inplace = True)
FufData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FufData['month']])
FufData = FufData.apply(pd.to_numeric).resample("M").mean()
FufData['month'] = FufData['month'].astype(int)
FufData = FufData.apply(pd.to_numeric).resample("M").mean()
FufData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FufData.index])


###############################################################################
FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M') 
                        for x in FwfData['Date']])
FwfData.set_index('Time', inplace = True, drop = True)
FwfData.replace(to_replace = -9999, value = np.nan, inplace = True) 

FwfData['month'] = ([datetime.datetime.strptime(x, '%m/%d/%Y %H:%M') 
                        for x in FwfData['Date']])
FwfData.drop(['Date'], axis = 1, inplace = True)
FwfData['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FwfData['month']])
FwfData = FwfData.apply(pd.to_numeric).resample("M").mean()
FwfData['month'] = FwfData['month'].astype(int)
FwfData = FwfData.apply(pd.to_numeric).resample("M").mean()
FwfData.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FwfData.index])


###############################################################################
FufFlux = '/home/tpham/Desktop/USFufFormatted.csv'
FufFluxData = pd.read_csv(FufFlux, header = 0)
FufFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufFluxData['Timestamp']])
FufFluxData.set_index('Time', inplace = True, drop = True)
Start = FufFluxData.index.get_loc((FufFluxData[FufFluxData['Timestamp'] == 200701010000]).iloc[0].name)
End = FufFluxData.index.get_loc((FufFluxData[FufFluxData['Timestamp'] == 200712312300]).iloc[0].name)
FufFluxDF = FufFluxData[Start:End]
FufFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

FufFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufFluxDF['Timestamp']])
FufFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FufFluxDF['month']])
FufFluxDF['month'].astype(float)
FufFluxDF = FufFluxDF.apply(pd.to_numeric).resample("M").sum()
FufFluxDF['month'] = FufFluxDF['month'].astype(int)

FufFluxDF = FufFluxDF[['P']]

FufFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FufFluxDF.index])

FufParition = FufData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]
FufParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)



fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
FufParition.plot.area(stacked = True, ax = ax1)
ax1.set_ylim((0, 0.4))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.16, 0.05))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 14, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.2)
ax2 = ax1.twinx()
ax2.invert_yaxis()
FufFluxDF['P'].plot.bar(ax=ax2, width = 0.1)
plt.xlim([0,11])
#plt.xlim([0,FufParition.size])
ax2.set_ylim((300, 0))
ax2.yaxis.set_ticks(np.arange(0, 101, 20))
ax2.set_ylabel("Precipitation [mm]", fontsize = 14, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.legend(loc = 'center right', fancybox = True, framealpha = 0.5,prop = {'size': 14})
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/FufPartition_2007.png", 
            bbox_inches='tight', pad_inches = 0.1)



###############################################################################
FwfFlux = '/home/tpham/Desktop/USFwfFormatted.csv'
FwfFluxData = pd.read_csv(FwfFlux, header = 0)
FwfFluxData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfFluxData['Timestamp']])
FwfFluxData.set_index('Time', inplace = True, drop = True)
Start = FwfFluxData.index.get_loc((FwfFluxData[FwfFluxData['Timestamp'] == 201001010000]).iloc[0].name)
End = FwfFluxData.index.get_loc((FwfFluxData[FwfFluxData['Timestamp'] == 201012312300]).iloc[0].name)
FwfFluxDF = FwfFluxData[Start:End]
FwfFluxDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

FwfFluxDF['month'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfFluxDF['Timestamp']])
FwfFluxDF['month'] = ([datetime.datetime.strftime(x, '%m') 
                        for x in FwfFluxDF['month']])
FwfFluxDF['month'].astype(float)
FwfFluxDF = FwfFluxDF.apply(pd.to_numeric).resample("M").sum()
FwfFluxDF['month'] = FwfFluxDF['month'].astype(int)

FwfFluxDF = FwfFluxDF[['P']]
FwfFluxDF.index = ([datetime.datetime.strftime(x, '%b') 
                        for x in FwfFluxDF.index])


FwfParition = FwfData[['Transpiration', 'EvaporationCanopy',
                       'EvaporationSoil']]

FwfParition.rename(columns = {'EvaporationCanopy': 'Wet Canopy Evaporation',
                              'EvaporationSoil': 'Soil Evaporation'}, inplace = True)

fig, ax1 = plt.subplots(1, 1, figsize=(20,12))
FwfParition.plot.area(stacked = True, ax = ax1)
ax1.set_ylim((0, 0.4))
ax1.minorticks_off()
ax1.yaxis.set_ticks(np.arange(0, 0.16, 0.05))
ax1.set_ylabel("ET Component [mm/hr]", fontsize = 14, fontweight = 'bold')
ax1.yaxis.set_label_coords(-0.05,0.2)
ax2 = ax1.twinx()
ax2.invert_yaxis()
FwfFluxDF['P'].plot.bar(ax=ax2, width = 0.1)
plt.xlim([0,11])
#plt.xlim([0,FufParition.size])
ax2.set_ylim((300, 0))
ax2.yaxis.set_ticks(np.arange(0, 101, 20))
ax2.set_ylabel("Precipitation [mm]", fontsize = 14, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.legend(loc = 'center right', fancybox = True, framealpha = 0.5,prop = {'size': 14})
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/FwfPartition_2007.png", 
            bbox_inches='tight', pad_inches = 0.1)



'''
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
#plt.xlim([0,FufParition.size])
ax2.set_ylim((300, 0))
ax2.yaxis.set_ticks(np.arange(0, 81, 10))
ax2.set_ylabel("Precipitation [mm]", fontsize = 14, fontweight = 'bold', rotation = 270)
ax2.yaxis.set_label_coords(1.05, 0.85)
ax1.legend(loc = 'center right', fancybox = True, framealpha = 0.5,prop = {'size': 14})
ax1.set_xlabel("Month", fontsize = 14, fontweight = 'bold')

plt.savefig("/home/tpham/Windows Share/Thesis_Figures/SrmPartition_2010.png", 
            bbox_inches='tight', pad_inches = 0.1)



'''


















