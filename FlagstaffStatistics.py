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



FufFile = '/home/tpham/Desktop/USFuf.csv'
FmfFile = '/home/tpham/Desktop/USFmf.csv'
FwfFile = '/home/tpham/Desktop/USFwf.csv'


FufData = pd.read_csv(FufFile, header = 2)
FmfData = pd.read_csv(FmfFile, header = 2)
FwfData = pd.read_csv(FwfFile, header = 2)

FufData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FufData['TIMESTAMP_START']])
FufData.set_index('Time', inplace = True, drop = True)

FwfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FwfData['TIMESTAMP_START']])
FwfData.set_index('Time', inplace = True, drop = True)

FmfData['Time'] = ([datetime.datetime.strptime(str(x), '%Y%m%d%H%M') 
                        for x in FmfData['TIMESTAMP_START']])
FmfData.set_index('Time', inplace = True, drop = True)





FwfIndexStart = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200901010000]).iloc[0].name)
FwfIndexEnd = FwfData.index.get_loc((FwfData[FwfData['TIMESTAMP_START'] == 200912312330]).iloc[0].name)
FwfDF = FwfData[FwfIndexStart:FwfIndexEnd]
FwfDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
FwfDF[['P']].sum()


FwfDF[['LE', 'H', 'G', 'SWC_1', 'TS_1', 'NETRAD']].mean()



Gfuf = [-1.21,-0.48,-0.57,0.36,-0.04]
GFmf = [-0.51,0.92,0.06,0.46,0.10]
GFwf = [0.65,2.75,2.32,1.37,0.38]

[x/y for x, y in zip(GFmf, Gfuf)]



FufNet = [105.49,106.98,119.61,120.80,122.78]
FwfNet = [68.91,66.39,64.15,62.23,63.89]
FmfNet = [104.16,109.17,118.84,111.16,117.39]

[x/y for x, y in zip(FufNet, FwfNet)]
[x/y for x, y in zip(FufNet, FmfNet)]

[x-y for x, y in zip(FufNet, FwfNet)]


FufIndexStart = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 201001010000]).iloc[0].name)
FufIndexEnd = FufData.index.get_loc((FufData[FufData['TIMESTAMP_START'] == 201012312330]).iloc[0].name)
FufDF = FufData[FufIndexStart:FufIndexEnd]
FufDF.replace(to_replace = -9999, value = np.nan, inplace = True) 
FufDF[['P']].sum()


FufDF[['LE', 'H', 'G_1_1_1', 'SWC_1_1_1', 'SWC_1_2_1', 'TS_1_1_1', 'TS_1_2_1', 'NETRAD']].mean()





#FmfIndexStart = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200606210000]).iloc[0].name)
#FmfIndexEnd = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200609192330]).iloc[0].name)

FmfIndexStart = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200601010000]).iloc[0].name)
FmfIndexEnd = FmfData.index.get_loc((FmfData[FmfData['TIMESTAMP_START'] == 200612312330]).iloc[0].name)
FmfDF = FmfData[FmfIndexStart:FmfIndexEnd]
FmfDF.replace(to_replace = -9999, value = np.nan, inplace = True)
FmfDF[['P']].sum()


FmfDF[['LE', 'H', 'G', 'SWC_1', 'TS_1', 'NETRAD']].mean()


























