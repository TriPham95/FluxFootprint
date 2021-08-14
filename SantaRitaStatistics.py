#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 11:07:54 2019

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

SrgIndexStart = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200801010000]).iloc[0].name)
SrgIndexEnd = SrgData.index.get_loc((SrgData[SrgData['TIMESTAMP_START'] == 200812312330]).iloc[0].name)
SrgDF = SrgData[SrgIndexStart:SrgIndexEnd]
SrgDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrgDF[['LE_F_MDS', 'H_F_MDS', 'G_F_MDS', 'SWC_1_1_1', 'SWC_1_6_1', 'TS_1_1_1', 'TS_1_6_1', 'NETRAD']].mean()


SrgDF[['P']].sum()




SrcIndexStart = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 201401010000]).iloc[0].name)
SrcIndexEnd = SrcData.index.get_loc((SrcData[SrcData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)
SrcDF = SrcData[SrcIndexStart:SrcIndexEnd]
SrcDF.replace(to_replace = -9999, value = np.nan, inplace = True) 

SrcDF[['LE_F_MDS', 'H_F_MDS', 'G_F_MDS', 'SWC_1', 'SWC_2', 'TS_1', 'TS_2', 'NETRAD']].mean()

SrcDF[['P']].sum()



SrmIndexStart = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 201401010000]).iloc[0].name)
SrmIndexEnd = SrmData.index.get_loc((SrmData[SrmData['TIMESTAMP_START'] == 201412312330]).iloc[0].name)
SrmDF = SrmData[SrmIndexStart:SrmIndexEnd]
SrmDF.replace(to_replace = -9999, value = np.nan, inplace = True)

SrmDF[['LE_F_MDS', 'H_F_MDS', 'G_F_MDS', 'SWC_PI_1_1_A', 
       'SWC_PI_1_8_A', 'TS_PI_1_1_A', 'TS_PI_1_8_A', 'NETRAD']].mean()

SrmDF[['P']].sum()


























