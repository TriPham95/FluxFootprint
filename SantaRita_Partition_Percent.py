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


SrgFile = '/home/tpham/Desktop/SrgDiurnal_validation.csv'
SrmFile = '/home/tpham/Desktop/SrmDiurnal_validation.csv'
SrcFile = '/home/tpham/Desktop/SrcDiurnal_validation.csv'


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



SrgData['EvaporationSoil'] / SrgData['ET']
SrgData['Transpiration'] / SrgData['ET']
SrgData['EvaporationCanopy'] / SrgData['ET']


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

SrmData['EvaporationSoil'] / SrmData['ET']
SrmData['Transpiration'] / SrmData['ET']
SrmData['EvaporationCanopy'] / SrmData['ET']



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

SrcData['EvaporationSoil'] / SrcData['ET']
SrcData['Transpiration'] / SrcData['ET']
SrcData['EvaporationCanopy'] / SrcData['ET']














































